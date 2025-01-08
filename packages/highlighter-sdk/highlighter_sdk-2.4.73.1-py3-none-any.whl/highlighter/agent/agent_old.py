import os
from typing import Callable, Optional, Tuple

import aiko_services as aiko
from aiko_services.main import StreamEvent
from aiko_services.main import aiko as aiko_main

__all__ = [
    "init_agent",
    "run_agent",
    "set_mock_aiko_messager",
]


class HLAgent(aiko.PipelineImpl):

    def __init__(self, context):
        self.hl_task_status_info = {
            "state": aiko.StreamState.RUN,
            "message": "",
        }
        self.on_agent_error: Optional[Callable] = None
        self.on_agent_stop: Optional[Callable] = None
        self.on_before_process_frame: Optional[Callable] = None
        self.on_after_process_frame: Optional[Callable] = None
        super().__init__(context)

    def _process_stream_event(self, element_name, stream_event, diagnostic, in_destroy_stream=False):
        # class StreamState:
        #    ERROR =   -2  # Don't generate new frames and ignore queued frames
        #    STOP  =   -1  # Don't generate new frames and process queued frames
        #    RUN   =    0  # Generate new frames and process queued frames

        most_recent_state = self.hl_task_status_info["state"]

        if stream_event == aiko.StreamEvent.ERROR:
            if aiko.StreamState.ERROR < most_recent_state:
                self.hl_task_status_info["state"] = aiko.StreamState.ERROR
                self.hl_task_status_info["message"] = diagnostic

        elif stream_event == aiko.StreamEvent.STOP:
            if aiko.StreamState.STOP < most_recent_state:
                self.hl_task_status_info["state"] = aiko.StreamState.STOP
                self.hl_task_status_info["message"] = diagnostic

        return super()._process_stream_event(
            element_name, stream_event, diagnostic, in_destroy_stream=in_destroy_stream
        )

    def process_frame(self, stream_dict, frame_data) -> Tuple[StreamEvent, dict]:
        try:
            if self.on_before_process_frame is not None:
                self.on_before_process_frame(self)
        except Exception as e:
            return StreamEvent.ERROR, {"diagnostic": e.message}

        result = self._process_frame_common(stream_dict, frame_data, True)

        try:
            if self.on_after_process_frame is not None:
                self.on_after_process_frame(self)
        except Exception as e:
            return StreamEvent.ERROR, {"diagnostic": e.message}

        return result

    def run_agent(self, *args, **kwargs):
        self.run(*args, **kwargs)

        hl_task_status = self.hl_task_status_info

        if (hl_task_status["state"] == aiko.StreamState.ERROR) and self.on_agent_error is not None:
            self.on_agent_error(self)
        elif (hl_task_status["state"] == aiko.StreamState.STOP) and self.on_agent_stop is not None:
            self.on_agent_stop(self)


aiko.PipelineImpl = HLAgent


def init_agent(definition_pathname, name):

    if not os.path.exists(definition_pathname):
        raise SystemExit(f"Error: PipelineDefinition not found: {definition_pathname}")

    pipeline_definition = aiko.PipelineImpl.parse_pipeline_definition(definition_pathname)
    name = name if name else pipeline_definition.name

    init_args = aiko.pipeline_args(
        name,
        protocol=aiko.PROTOCOL_PIPELINE,
        definition=pipeline_definition,
        definition_pathname=definition_pathname,
    )
    pipeline = aiko.compose_instance(aiko.PipelineImpl, init_args)

    return pipeline, pipeline_definition


def run_agent(pipeline, stream_id, stream_parameters):

    pipeline.create_stream(stream_id, dict(stream_parameters))


def set_mock_aiko_messager():
    # ToDo: Chat with Andy about if this is a requirement. The issue is
    # in pipeline.py +999 causes an error because if I use `process_frame`
    # directly, without setting the aiko.message object to something I
    # get an attribute error when .publish is called
    class MockMessage:
        def publish(self, *args, **kwargs):
            pass

        def subscribe(self, *args, **kwargs):
            pass

        def unsubscribe(self, *args, **kwargs):
            pass

    aiko_main.message = MockMessage()
