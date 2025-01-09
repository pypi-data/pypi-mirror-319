#!/usr/bin/env python3
from dataclasses import dataclass

@dataclass(kw_only=True)
class Node():
    leaves: list
    key: str
    value: int | None

class ReplyTree():
    def __init__(self):
        self.__root = Node(
            leaves=[], key="", value=None
        )

    def __get(self, reply: str):
        current: Node = self.__root
        index: int = 0

        while index < len(reply):
            char: str = reply[index]
            for node in current.leaves:
                if node.key == char:
                    current = node
                    index = index + 1
                    break
            else:
                return index, current
        else:
            return index, current

    def get(self, reply: str):
        _, node = self.__get(reply)
        return node.value

    def insert(self, message: str, id: int):
        index, node = self.__get(message)
        node.leaves.append(Node(leaves=[], key=message[index], value=id))
