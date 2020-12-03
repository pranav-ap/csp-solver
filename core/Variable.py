from typing import Union

ValueType = Union[str, int]


class Variable:
    def __init__(self, name: str) -> None:
        self.name = name
        self.value: ValueType = None

    def set_value(self, value) -> None:
        self.value = value

    def __repr__(self):
        return ' '.join([self.name, self.value])
