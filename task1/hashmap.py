from typing import Hashable, Any


class Node:
    def __init__(self, key: Hashable, value: Any):
        self.key = key
        self.value = value
        self.next: None | Node = None


class HashMap:
    """Hash map using the separate chaining approach"""

    def __init__(self, capacity: int = 16, load_factor: float = 0.75):
        self.capacity = capacity
        self.load_factor = load_factor
        self.size: int = 0
        self.data: list[Node | None] = [None] * self.capacity

    def get(self, key: Hashable) -> Node | None:
        """
        Retrieve the node associated with the given key.
        """
        current_node, _ = self._get(key=key)
        return current_node

    def set(self, key: Hashable, value: Any) -> Node:
        """
        Insert key-value pair in the hashmap or raise
        `KeyError` if node with the same key already exists.
        """
        current_node, parent_node = self._get(key=key)

        if current_node:
            raise KeyError(
                "You already have an object with the "
                "same key if you want update it use 'put' instead"
            )

        index = self._get_index(key=key)
        new_node = Node(key=key, value=value)

        if parent_node:
            parent_node.next = new_node
        else:
            self.data[index] = new_node

        self.size += 1

        if self.size > self.capacity * self.load_factor:
            self._resize()

        return new_node

    def put(self, key: Hashable, value: Any) -> Node | None:
        """
        Update the value of the node
        associated with the given key, if it exists.
        """
        current_node, _ = self._get(key=key)

        if current_node:
            current_node.value = value
            return current_node

    def delete(self, key: Hashable) -> None:
        """
        Delete the node associated with the given key from the hashmap.
        """
        current_node, parent_node = self._get(key=key)

        if current_node:
            # If the node to delete is the head of the linked list
            if not parent_node:
                self.data[self._get_index(key)] = current_node.next
            else:
                parent_node.next = current_node.next
            self.size -= 1

    def _get_index(self, key: Hashable) -> int:
        """
        Calculate the index in the hashmap for the given key.
        """
        return hash(key) % self.capacity

    def _resize(self) -> None:
        """
        Resize the hash map to increase its capacity.
        """
        entries = [(key, value) for key, value in self]

        self.capacity *= 2
        self.size = 0
        self.data = [None] * self.capacity

        for entry in entries:
            key, value = entry
            self.set(key=key, value=value)

    def _get(self, key: Hashable) -> tuple[Node | None, Node | None]:
        """
        Retrieve the node associated with the given key and its parent node.
        """
        index = self._get_index(key)
        current_node = self.data[index]
        parent_node = None

        while current_node and current_node.key != key:
            parent_node = current_node
            current_node = current_node.next

        return current_node, parent_node

    def __iter__(self):
        """
        Iterate over all key-value pairs of nodes stored in the hash map.
        """
        for node in self.data:
            while node:
                yield node.key, node.value
                node = node.next
