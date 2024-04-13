import unittest
from unittest.mock import patch

from hashmap import HashMap, Node


class HashMapTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.hashmap = HashMap()
        self.key = "Color"
        self.value = "Black"

    def test_protected_get_index_int_lt_capacity(self):
        index = self.hashmap._get_index(key=self.key)

        self.assertLess(index, self.hashmap.capacity)
        self.assertIsInstance(index, int)

    def test_protected_get_by_existing_key(self):
        index = self.hashmap._get_index(key=self.key)
        existing_node = Node(key=self.key, value=self.value)
        self.hashmap.data[index] = existing_node

        expected_result = existing_node, None
        result = self.hashmap._get(key=self.key)

        self.assertEqual(result, expected_result)

    def test_protected_get_by_not_existing_key(self):
        expected_result = None, None
        result = self.hashmap._get(key=self.key)

        self.assertEqual(result, expected_result)

    @patch.object(HashMap, "_get_index")
    def test_protected_get_parent_node(self, mock_get_index):
        mock_get_index.return_value = 0

        parent_key, parent_value = "Quality", "Good"
        index = self.hashmap._get_index(key=parent_key)

        parent_node = Node(key=parent_key, value=parent_value)
        searching_node = Node(key=self.key, value=self.value)
        parent_node.next = searching_node

        self.hashmap.data[index] = parent_node

        expected_result = (searching_node, parent_node)
        result = self.hashmap._get(key=self.key)

        self.assertEqual(result, expected_result)

    def test_magic_method_iter(self):
        index = self.hashmap._get_index(key=self.key)
        existing_node = Node(key=self.key, value=self.value)

        self.hashmap.data[index] = existing_node

        expected_result = [(existing_node.key, existing_node.value)]
        result = [node for node in self.hashmap]

        self.assertEqual(result, expected_result)

    def test_protected_resize_doubling_capacity(self):
        expected_result_capacity = self.hashmap.capacity * 2

        for i in range(
                int(
                    self.hashmap.capacity
                    * self.hashmap.load_factor
                ) + 1):
            self.hashmap.set(key=f"{self.key}-{i}", value=f"{self.value}-{i}")

        result_capacity = self.hashmap.capacity

        self.assertEqual(result_capacity, expected_result_capacity)

    def test_get_by_existing_key(self):
        existing_node = Node(key=self.key, value=self.value)
        index = self.hashmap._get_index(key=self.key)

        self.hashmap.data[index] = existing_node

        expected_result = existing_node
        result = self.hashmap.get(key=self.key)

        self.assertEqual(result, expected_result)

    def test_get_by_not_existing_key(self):
        expected_result = None
        result = self.hashmap.get(key=self.key)

        self.assertEqual(result, expected_result)

    def test_set_can_set_not_existing_key(self):
        self.hashmap.set(key=self.key, value=self.value)

        result = [
            self.hashmap.get(key=self.key).key,
            self.hashmap.get(key=self.key).value,
        ]
        expected_result = [self.key, self.value]

        self.assertEqual(result, expected_result)

    def test_set_cant_set_existing_key(self):
        self.hashmap.set(key=self.key, value=self.value)

        expected_exception = KeyError

        with self.assertRaises(expected_exception):
            self.hashmap.set(key=self.key, value=self.value)

    def test_set_change_size(self):
        expected_result = self.hashmap.size + 1

        self.hashmap.set(key=self.key, value=self.value)

        result = self.hashmap.size

        self.assertEqual(result, expected_result)

    @patch.object(HashMap, "_get_index")
    def test_set_handle_collisions(self, mock_get_index):
        mock_get_index.return_value = 0

        same_index_key, same_index_value = "Quality", "Good"

        self.hashmap.set(key=self.key, value=self.value)
        self.hashmap.set(key=same_index_key, value=same_index_value)

        result_1 = [
            self.hashmap.get(key=self.key).key,
            self.hashmap.get(key=self.key).value,
        ]
        result_2 = [
            self.hashmap.get(key=same_index_key).key,
            self.hashmap.get(key=same_index_key).value,
        ]

        expected_result_1 = [self.key, self.value]
        expected_result_2 = [same_index_key, same_index_value]

        result_node = self.hashmap.get(key=self.key).next
        expected_result_node = self.hashmap.get(key=same_index_key)

        self.assertEqual(result_1, expected_result_1)
        self.assertEqual(result_2, expected_result_2)
        self.assertEqual(result_node, expected_result_node)

    def test_put_by_existing_key(self):
        new_value = "White"

        self.hashmap.set(key=self.key, value=self.value)

        expected_result = new_value
        result = self.hashmap.put(key=self.key, value=new_value).value

        self.assertEqual(result, expected_result)

    def test_put_by_not_existing_key(self):
        self.hashmap.put(key=self.key, value=self.value)

        expected_result = None
        result = self.hashmap.put(key=self.key, value=self.value)

        self.assertEqual(result, expected_result)

    def test_delete_by_existing_key(self):
        self.hashmap.set(key=self.key, value=self.value)
        self.hashmap.delete(key=self.key)

        expected_result = None
        result = self.hashmap.get(key=self.key)

        self.assertEqual(result, expected_result)

    def test_delete_change_size(self):
        self.hashmap.set(key=self.key, value=self.value)

        expected_result = self.hashmap.size - 1

        self.hashmap.delete(key=self.key)

        result = self.hashmap.size

        self.assertEqual(result, expected_result)

    def test_delete_by_not_existing_key(self):
        key = "Black"

        expected_result = self.hashmap.size

        self.hashmap.delete(key=key)

        result = self.hashmap.size

        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
