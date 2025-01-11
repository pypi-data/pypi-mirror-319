from pathlib import Path
from chatollama import Engine, Conversation, Event, StreamEvent
from chatollamaagent import NetworkRunner


class LuciusAgent:
    def __init__(self):
        self.network_path = Path(__file__, "..", "lucius_network.coa")
        self.network_runner = NetworkRunner(self.network_path)
        # self.network_runner.run()
        self.network_runner.lucius_agent = self

        self.lucius_prompt_path = Path(__file__, "..", "lucius_prompt.md")
        self.lucius_prompt = open(
            self.lucius_prompt_path, "r", encoding="utf-8").read()
        self.engine = Engine(model="llama3.1:8b")
        self.engine.stream = True
        self.engine.stream_event.on(self.stream_event)

        self.response_mode_switch_event = Event()
        self.chat_response_event = Event()
        self.function_call_event = Event()

        self.lucius_start_tag = "<lucius:function_calls>"
        self.lucius_end_tag = "</lucius:function_calls>"
        self.reset()
        self.clear()

    def clear(self):
        self.chat_response = ""
        self.function_response = ""
        self.accumulated_response = ""
        self.response_mode = "chat"

    def reset(self):
        self.engine.conversation = Conversation()
        self.engine.conversation.system(self.lucius_prompt)

    def message(self, message: str) -> str:
        self.engine.user(message)
        self.engine.chat()
        response = self.engine.response
        self.engine.assistant(response)
        print(message)
        print(response)
        return response

    def stream_event(self, event: StreamEvent) -> None:
        delta = event.delta
        if event.mode == 0:
            self.clear()
        if event.mode == 1:
            self.accumulated_response += delta
            if self.response_mode == "chat":
                self.chat_response += delta
                self.chat_response_event.trigger(event)
                if self.lucius_start_tag in self.accumulated_response:
                    self.response_mode = "function"
                    self.accumulated_response = self.accumulated_response.replace(
                        self.lucius_start_tag, "")
                    self.chat_response = self.chat_response.replace(
                        self.lucius_start_tag, "")
                    self.function_response = self.lucius_start_tag
                    self.response_mode_switch_event.trigger()
            elif self.response_mode == "function":
                self.function_response += delta
                self.function_call_event.trigger(event)
                if self.lucius_end_tag in self.accumulated_response:
                    self.engine.stream_stop = True
                    self.accumulated_response = self.accumulated_response.replace(
                        self.lucius_end_tag, "")
