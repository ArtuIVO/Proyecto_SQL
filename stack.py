from nudo import Node
from comida import Comida


class Stack:
    def __init__(self, limit: int | None = None):
        self.size = 0
        self.max = limit
        self.head: Node | None = None

    def prepend(self, data: Comida):
        if self.size == self.max:
            raise Exception("Desbordamiento de pila")
        else:
            new_node = Node(data)
            new_node.next = self.head
            self.head = new_node
            self.size += 1

    def shift(self):
        if self.head is None:
            raise Exception("Subdesvordamiento de pila")
        else:
            current = self.head
            self.head = current.next
            current.next = None
            self.size -= 1

            return current.data

    def transversal(self):
        current = self.head
        result = ""
        while current is not None:
            result += str(current)
            current = current.next

            if current is not None:
                result += "->"

        return result
