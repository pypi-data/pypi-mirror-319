#!/usr/bin/env python3

from dataclasses import dataclass

@dataclass(kw_only=True)
class Node():
    leaves: dict
    value: int | None

class ReplyTree():
    def __init__(self):
        self.__root = Node(
            leaves=dict(), value=None
        )

    def __get(self, reply: str) -> tuple[int, Node]:
        current: Node = self.__root
        index: int = 0

        while index < len(reply):
            char: str = reply[index]
            next = current.leaves.get(char)

            if next:
                index = index + 1
                current = next
            else:
                return index, current

        return index, current

    def get(self, reply: str) -> int | None:
        _, node  = self.__get(reply)
        return node.value

    def insert(self, message: str, id: int) -> None:
        index, node = self.__get(message)
        node.leaves[message[index]] = Node(leaves=dict(), value=id)

tree = ReplyTree()

msg1 = "t1"
value1 = 1

msg2 = "t2"
value2 = 2

tree.insert(msg1, value1)
tree.insert(msg2, value2)

print(tree.get(msg1))
print(tree.get(msg2))
