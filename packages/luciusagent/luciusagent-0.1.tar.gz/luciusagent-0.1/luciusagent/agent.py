from pathlib import Path
from chatollama import Engine, Conversation, StreamEvent


class LuciusAgent:
    def __init__(self):
        self.lucius_prompt_path = Path(__file__, "..", "lucius_prompt.md")
        self.lucius_prompt = open(
            self.lucius_prompt_path, "r", encoding="utf-8").read()
        self.engine = Engine(model="llama3.1:8b")
        self.engine.stream = True
        self.engine.stream_event.on(self.stream_event)
        self.reset()
        self.clear()

    def clear(self):
        self.chat_response = ""
        self.function_response = ""
        self.response_mode = "chat"

    def reset(self):
        self.engine.conversation = Conversation()
        self.engine.conversation.system(self.lucius_prompt)

    def message(self, message: str) -> str:
        self.engine.conversation.user(message)
        self.engine.chat()
        print(self.chat_response)
        print("--------------------------------")
        print(self.function_response)
        response = self.engine.response
        return response


    def stream_event(self, event: StreamEvent) -> None:
        delta = event.delta
        text = event.text
        if event.mode == 0:
            self.clear()
        if event.mode == 1:
            if "<lucius:function_calls>" in delta:
                self.response_mode = "function"
            elif "</lucius:function_calls>" in delta and self.response_mode == "function":
                self.response_mode = "chat"
                self.engine.stream_stop = True
                return
            
            if self.response_mode == "chat":
                self.chat_response += delta
            else:
                self.function_response += delta

