from chatollamaagent.nodes.base import Node, NodeInstance, node
from chatollamaagent.nodes.builtin import TextSocket, DataSocket, socket, StringSocket
from .agent import LuciusAgent


@socket()
class LuciusSocket(DataSocket):
    color = "#D69E21"

    @classmethod
    def init_socket(cls) -> None:
        cls.add_to_white_list(cls)


@node()
class CreateLuciusNode(Node):
    _title = "Create Lucius"
    _category = "!Lucius"
    _header_color = "#A57C21"
    _background_color = "#6D4B12"

    def __init__(self):
        super().__init__()

        self.add_socket("Lucius", "output", LuciusSocket)

    def execute(self, node_instance: NodeInstance) -> None:
        node_instance.lucius_agent = LuciusAgent()
        node_instance.set_socket_value(
            "Lucius", "output", node_instance.lucius_agent)


@node()
class MessageLuciusNode(Node):
    _title = "Message Lucius"
    _category = "!Lucius"
    _header_color = "#A57C21"
    _background_color = "#6D4B12"

    def __init__(self):
        super().__init__()

        self.add_socket("Lucius", "input", LuciusSocket)
        self.add_socket("Message", "input", TextSocket)
        self.add_socket("Lucius", "output", LuciusSocket)
        self.add_socket("Response", "output", TextSocket)

    def execute(self, node_instance: NodeInstance) -> None:
        lucius_agent: LuciusAgent = node_instance.get_socket_value(
            "Lucius", "input")
        message: str = node_instance.get_socket_value("Message", "input")

        response = lucius_agent.message(message)

        node_instance.set_socket_value("Response", "output", response)
        node_instance.set_socket_value("Lucius", "output", lucius_agent)


@node()
class ResetLuciusNode(Node):
    _title = "Reset Lucius"
    _category = "!Lucius"
    _header_color = "#A57C21"
    _background_color = "#6D4B12"

    def __init__(self):
        super().__init__()

        self.add_socket("Lucius", "input", LuciusSocket)
        self.add_socket("Lucius", "output", LuciusSocket)

    def execute(self, node_instance: NodeInstance) -> None:
        lucius_agent: LuciusAgent = node_instance.get_socket_value(
            "Lucius", "input")

        lucius_agent.reset()
        node_instance.set_socket_value("Lucius", "output", lucius_agent)


@node()
class GetLuciusPromptNode(Node):
    _title = "Get Lucius Prompt"
    _category = "!Lucius"
    _header_color = "#A57C21"
    _background_color = "#6D4B12"

    def __init__(self):
        super().__init__()

        self.add_socket("Lucius", "input", LuciusSocket)
        self.add_socket("Prompt", "output", TextSocket)
        self.add_socket("Lucius", "output", LuciusSocket)

    def execute(self, node_instance: NodeInstance) -> None:
        lucius_agent: LuciusAgent = node_instance.get_socket_value(
            "Lucius", "input")

        prompt = lucius_agent.lucius_prompt
        node_instance.set_socket_value("Prompt", "output", prompt)
        node_instance.set_socket_value("Lucius", "output", lucius_agent)

@node()
class SetLuciusPromptNode(Node):
    _title = "Set Lucius Prompt"
    _category = "!Lucius"
    _header_color = "#A57C21"
    _background_color = "#6D4B12"

    def __init__(self):
        super().__init__()

        self.add_socket("Lucius", "input", LuciusSocket)
        self.add_socket("Prompt", "input", TextSocket)
        self.add_socket("Lucius", "output", LuciusSocket)

    def execute(self, node_instance: NodeInstance) -> None:
        lucius_agent: LuciusAgent = node_instance.get_socket_value(
            "Lucius", "input")
        prompt = node_instance.get_socket_value("Prompt", "input")

        lucius_agent.lucius_prompt = prompt
        node_instance.set_socket_value("Lucius", "output", lucius_agent)


@node()
class JoinTextNode(Node):
    _title = "Join Text"
    _category = "!Lucius"
    _header_color = "#A57C21"
    _background_color = "#6D4B12"

    def __init__(self):
        super().__init__()

        self.add_socket("Text A", "input", TextSocket)
        self.add_socket("Separator", "input", StringSocket)
        self.add_socket("Text B", "input", TextSocket)
        self.add_socket("Text", "output", TextSocket)

    def execute(self, node_instance: NodeInstance) -> None:
        text_a = node_instance.get_socket_value("Text A", "input")
        separator = node_instance.get_socket_value("Separator", "input")
        text_b = node_instance.get_socket_value("Text B", "input")

        text = f"{text_a}{separator}{text_b}"

        node_instance.set_socket_value("Text", "output", text)
