from nudo import Node
from usuario import Usuarios
from cliente import Cliente


class Lista:
    def __init__(self, limit: int | None = None):
        self.size = 0
        self.max = limit
        self.head: Node | None = None
        self.tail: Node | None = None

    def __getitem__(self, index):
        current = self.head
        count = 0

        while current is not None:
            if count == index:
                return current.data
            else:
                current = current.next
                count += 1

        raise IndexError("Index out of range")

    def preprend(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1

    def preprend_usuarios(self, data: Usuarios):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1

    def is_empty(self):
        return self.head is None and self.tail is None

    def append(self, data):
        if self.is_empty():
            new_node = Node(data)
            self.head = new_node
            self.tail = new_node
            self.size += 1
        else:
            new_node = Node(data)
            self.tail.next = new_node
            self.tail = new_node
            self.size += 1

    def search_by_ID(self, data: int):
        current = self.head

        while current is not None:
            if isinstance(current.data, Usuarios) and current.data.identificador == data:
                return current
            else:
                current = current.next

        return None

    def shift(self):
        if self.head is None:
            raise Exception("Subdesvordamiento de pila")
        else:
            current = self.head
            self.head = current.next
            current.next = None
            self.size -= 1

            return current.data

    def search_by_position(self, data: int):
        current = self.head
        current_data = 0

        while current is not None:
            if current_data == data:
                return current
            else:
                current = current.next
                current_data += 1

        raise Exception("The position is not exist")

    def search_by_node_position(self, ref: Node):
        current = self.head
        current_data = 0

        while current is not None:
            if current == ref:
                return current_data
            else:
                current = current.next
                current_data += 1

        raise Exception("The position is not exist")

    def deleate_by_ID(self, data: int):
        current = self.head
        previous = None

        while current is not None:
            if isinstance(current.data, Usuarios) and current.data.identificador == data:
                if previous is None:
                    return self.shift()
                else:
                    previous.next = current.next
                    current.next = None
                    self.size -= 1
                    return current.data

            previous = current
            current = current.next

        raise Exception("Not found this element")

    def pop(self):
        if self.tail is None:
            raise Exception("Subdesbordamiento de lista")
        elif self.head is self.tail:
            current = self.head
            self.head = None
            self.tail = None
            self.size = 0
            return current.data
        else:
            current = self.tail
            self.tail = current
            previous = self.search_by_position(self.size - 2)
            previous.next = None

            return current.data

    def transversal(self):
        current = self.head
        result = ""
        while current is not None:
            result += str(current)
            current = current.next

            if current is not None:
                result += " --> \n"
        return result
