"""The pulseaudio interface."""

import asyncio
import logging
from pathlib import Path

from libpulse.libpulse import (LibPulse, PA_SUBSCRIPTION_MASK_SINK_INPUT,
                               LibPulseStateError)
from .upnp.util import NL_INDENT, log_unhandled_exception

logger = logging.getLogger('pulse')

APPS_TITLE = 'Application name -> uuid'
APPS_HEADER = f"""# List of 'application name -> DLNA device uuid'.
#
# This list is generated by pa-dlna when run with the '--clients-uuids'
# command line option. You may remove a line or comment it out (using the '#'
# character as the line prefix) to remove the association between an
# application and a device.

# Default section header.
# DO NOT change the next line.
[{APPS_TITLE}]

"""

# Classes.
class NullSink:
    """A connection between a sink_input and the null-sink of a Renderer.

    A NullSink is instantiated upon registering a Renderer instance.
    """

    def __init__(self, sink):
        self.sink = sink        # libpulse Sink instance
        self.sink_input = None  # libpulse SinkInput instance

class SinkInputEvent:
    def __init__(self, sink_input, event):
        self.type = event.type
        # 'sink' is the index of the sink associated with the sink-input.
        self.sink = sink_input.sink
        self.proplist = sink_input.proplist

    def __eq__(self, other):
        return (self.type == other.type and
                self.sink == other.sink and
                self.proplist == other.proplist)

class Pulse:
    """Pulse monitors pulseaudio sink-input events."""

    def __init__(self, av_control_point):
        self.av_control_point = av_control_point
        self.clients_uuids = av_control_point.clients_uuids
        self.applications = av_control_point.applications
        self.closing = False
        self.lib_pulse = None
        self.sink_input_events = {}

    async def close(self):
        if not self.closing:
            self.closing = True
            logger.info('Close pulse')
            await self.av_control_point.close()

    async def get_sink(self, renderer, module_index, module_name):
        """Get the sink matching a renderer from 'module_index'."""

        for sink in await self.lib_pulse.pa_context_get_sink_info_list():
            if sink.owner_module == module_index:
                logger.info(f'Load null-sink module {sink.name}'
                        f"{NL_INDENT}description='{renderer.description}'")

                # The module name is registered by pulseaudio after being
                # modified in pa_namereg_register() by replacing invalid
                # characters with '_'. The invalid characters are defined in
                # is_valid_char(char c).See the pulseaudio code.
                if len(module_name) != len(sink.name):
                    # Pulseaudio has added a '.n' suffix because there exists
                    # another null-sink with the same name.
                    await self.lib_pulse.pa_context_unload_module(module_index)
                    renderer.control_point.abort(
                        f'Two DLNA devices registered with the same name:'
                        f'{NL_INDENT}{module_name}')

                    # AVControlPoint.abort() raises an exception.
                    assert False, 'Statement never reached'

                return sink

    async def register(self, renderer):
        """Load a null-sink module."""

        if self.lib_pulse is None:
            return

        upnp_device = renderer.upnp_device
        module_name = f'{renderer.getattr("modelName")}-{upnp_device.UDN}'
        _description = renderer.description.replace(' ', r'\ ')

        module_index = await self.lib_pulse.pa_context_load_module(
            'module-null-sink',
            f'sink_name="{module_name}" '
            f'sink_properties=device.description=' f'"{_description}"')

        # Return the NullSink instance.
        exception = None
        try:
            sink = await self.get_sink(renderer, module_index, module_name)
            if sink:
                return NullSink(sink)
        except Exception as e:
            exception = e

        await self.lib_pulse.pa_context_unload_module(module_index)
        logger.error(
            f'Failed loading {module_name} pulseaudio module')
        if exception:
            raise exception
        return None

    async def unregister(self, nullsink):
        if self.lib_pulse is None:
            return
        logger.info(f'Unload null-sink module {nullsink.sink.name}')
        await self.lib_pulse.pa_context_unload_module(
                                                nullsink.sink.owner_module)

    async def get_sink_input(self, renderer):
        assert renderer.nullsink is not None
        sink_inputs = (await
                       self.lib_pulse.pa_context_get_sink_input_info_list())
        for sink_input in sink_inputs:
            if sink_input.sink == renderer.nullsink.sink.index:
                return sink_input
        return None

    def is_ignored_event(self, sink_input, event):
        index = event.index
        if index not in self.sink_input_events:
            self.sink_input_events[index] = SinkInputEvent(sink_input, event)
            return False
        else:
            if event.type == 'remove':
                del self.sink_input_events[index]
            else:
                last_event = self.sink_input_events[index]
                new_event = SinkInputEvent(sink_input, event)
                if new_event == last_event:
                    return True     # Ignore the event.
                else:
                    self.sink_input_events[index] = new_event
        return False

    def find_previous_renderer(self, event):
        """Find the renderer that was last connected to this sink-input."""

        for renderer in self.av_control_point.renderers():
            if (renderer.nullsink is not None and
                    renderer.nullsink.sink_input is not None and
                    renderer.nullsink.sink_input.index == event.index):
                return renderer

    async def find_renderer(self, event):
        """Find the renderer now connected to this sink-input."""

        notfound = (None, None)

        # Find the sink_input that has triggered the event.
        # Note that by the time this code is running, pulseaudio may have done
        # other changes. In other words, there may be inconsistencies between
        # the event and the sink_input and sink lists.
        sink_inputs = (await
                       self.lib_pulse.pa_context_get_sink_input_info_list())
        for sink_input in sink_inputs:
            if sink_input.index == event.index:
                # Ignore 'pulsesink probe' - seems to be used to query sink
                # formats (not for playback).
                if sink_input.name == 'pulsesink probe':
                    return notfound

                # Find the corresponding sink when it is the null-sink of a
                # Renderer.
                for renderer in self.av_control_point.renderers():
                    if (renderer.nullsink is not None and
                            renderer.nullsink.sink.index == sink_input.sink):
                        return renderer, sink_input
                break
        return notfound

    async def dispatch_event(self, event):
        """Dispatch the event to a renderer.

        event.type is either 'new', 'change' or 'remove'.
        A new event.index is generated by pulseaudio for each 'new' event. The
        index of a 'remove' event refers to the index of a previous 'new'
        event.

        A 'new' event establishes an association between a sink-input and
        a sink.

        IMPORTANT:
        'nullsink.sink' and 'nullsink.sink_input' are the renderer's instances
        built from one of the previous events. They are stale instances.
        'sink' and 'sink_input' returned by find_renderer() and
        get_sink_by_name() are the current instances as set by pulseaudio.
        """

        evt_type = event.type
        if evt_type == 'remove':
            renderer = self.find_previous_renderer(event)
            if renderer is not None:
                renderer.pulse_queue.put_nowait((evt_type, None, None))
            return

        renderer, sink_input = await self.find_renderer(event)
        if renderer is not None:
            assert sink_input is not None

            # Ignore sound settings events.
            # See src/pulse/proplist.h in Pulseaudio source code.
            proplist = sink_input.proplist
            if (proplist and 'media.role' in proplist and
                    proplist['media.role'] == 'event'):
                return

            # 'renderer.nullsink.sink' is the stale sink from the previous
            # event, we need to fetch the 'sink' correponding to this event.
            sink = await self.lib_pulse.pa_context_get_sink_info_by_name(
                                                renderer.nullsink.sink.name)
            if sink is not None:
                if (self.is_ignored_event(sink_input, event) and
                        event.type not in ('new', 'remove')):
                    # Ignore a SinkInputEvent with no changes from the
                    # previous one (or if the previous one does not exist) and
                    # the event type is `change`.
                    pass
                elif sink_input.index == renderer.previous_idx:
                    # Ignore event related to the previous sink-input.
                    pass
                else:
                    renderer.pulse_queue.put_nowait(
                                                (evt_type, sink, sink_input))

        prev_renderer = self.find_previous_renderer(event)
        # The sink_input has been re-routed to another sink.
        if prev_renderer is not None and prev_renderer is not renderer:
            # Build our own 'exit' event (pulseaudio does not provide one)
            # for the sink that had been previously connected to this
            # sink_input.
            evt_type = 'exit'
            if event.index in self.sink_input_events:
                del self.sink_input_events[event.index]
            prev_renderer.pulse_queue.put_nowait((evt_type, None, None))

    def add_application(self, renderer, name, uuid):
        if self.applications is None:
            return
        if name not in self.applications or self.applications[name] != uuid:
            logger.info(f"Adding new association '{name}' ->"
                        f" uuid of '{renderer.name}'")
            self.applications[name] = uuid

    def write_applications(self):
        if not self.clients_uuids:
            return

        path = Path(self.clients_uuids)
        path = path.expanduser()
        try:
            with open(path, 'w') as f:
                f.write(APPS_HEADER)
                for k, val in self.applications.items():
                    indent = ' ' * max(20 - len(k), 1)
                    f.write(f'{k}{indent}-> {val}\n')
        except Exception as e:
            logger.exception(f'Error writing {path}: {e!r}')

    async def get_client(self, sink_input):
        if sink_input is None:
            return
        return await self.lib_pulse.pa_context_get_client_info(
                                                        sink_input.client)

    async def move_sink_input(self, sink_input, sink):
        await self.lib_pulse.pa_context_move_sink_input_by_index(
                                                sink_input.index, sink.index)

    async def find_sink_input(self, uuid):
        if self.applications is None:
            return
        lp = self.lib_pulse
        sink_inputs = await lp.pa_context_get_sink_input_info_list()
        for sink_input in sink_inputs:
            client = await self.get_client(sink_input)
            if client is None:
                continue
            app_name = client.proplist.get('application.name')
            if app_name is not None and self.applications.get(app_name) == uuid:
                return sink_input

    @log_unhandled_exception(logger)
    async def run(self):
        try:
            async with LibPulse('pa-dlna') as self.lib_pulse:
                # Only one instance of pa-dlna is allowed to run.
                n = len([client for client in
                        await self.lib_pulse.pa_context_get_client_info_list()
                                                if client.name == 'pa-dlna'])
                if n > 1:
                    logger.warning(
                        'There is already one instance of pa-dlna running')
                    return

                await self.lib_pulse.log_server_info()

                # Start the iteration on sink-input events.
                await self.lib_pulse.pa_context_subscribe(
                                    PA_SUBSCRIPTION_MASK_SINK_INPUT)
                iterator = self.lib_pulse.get_events_iterator()
                self.av_control_point.start_event.set()
                async for event in iterator:
                    await self.dispatch_event(event)

                # Wait until end of test.
                test_end = self.av_control_point.test_end
                if test_end is not None:
                    await test_end

        except LibPulseStateError as e:
            logger.error(f'{e!r}')
        finally:
            self.write_applications()
            self.lib_pulse = None
            await self.close()
