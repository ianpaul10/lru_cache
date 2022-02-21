import unittest
from src.ec_lru_cache import Node, LRUCache

class NodeBasicTests(unittest.TestCase):
    def test_node_init(self):
        expected_key = 5
        expected_val = "node_val_5"
        actual = Node(expected_key, expected_val)

        self.assertEqual(actual.key, expected_key)
        self.assertEqual(actual.val, expected_val)
        self.assertIsNone(actual.prev_node)
        self.assertIsNone(actual.next_node)

class LRUCacheBasicTests(unittest.TestCase):
    def setUp(self) -> None:
        self.cache = LRUCache(10)

    def test_get_key_does_not_exist(self):
        val = self.cache.get(5)
        self.assertIsNone(val)

    def test_basic_get_put(self):
        expected_node = Node(7, "node_val_7")
        expected_node.prev_node = Node(0, "head")
        expected_node.next_node = Node(0, "tail")

        self.cache.put(7, "node_val_7")

        actual = self.cache.get(7)

        self.assertEqual(actual.key, expected_node.key)
        self.assertEqual(actual.val, expected_node.val)
        self.assertEqual(actual.next_node.key, expected_node.next_node.key)
        self.assertEqual(actual.prev_node.key, expected_node.prev_node.key)

    def test_put_update(self):
        self.cache.put(3, "node_val_3")
        self.cache.put(3, "updated_node_val_3")
        expected = "updated_node_val_3"

        actual = self.cache.get(3)
        self.assertEqual(actual.val, expected)

class LRUCacheCapTests(unittest.TestCase):
    def setUp(self) -> None:
        # Set cache cap to 3, so we can see how it will function
        # if/when the cap is hit
        self.cache = LRUCache(3)

        # 1 is actually the LRU item after being added first
        self.cache.put(1, "node_val_1")
        self.cache.put(2, "node_val_2")

    def test_put_over_limit(self):
        # currently at 2, if we add 2 more, item 1 will get popped
        self.assertEqual(len(self.cache.node_dict), 2)
        
        self.cache.put(3, "node_val_3")
        self.assertEqual(len(self.cache.node_dict), 3)

        self.cache.put(4, "node_val_4")

        # this should now no longer exist
        item_1 = self.cache.get(1)

        self.assertEqual(len(self.cache.node_dict), 3)
        self.assertIsNone(item_1)

    def test_put_duplicates(self):
        # currently at 2, if we add 2 more, item 1 will get popped
        self.assertEqual(len(self.cache.node_dict), 2)
        
        self.cache.put(3, "node_val_3")
        self.assertEqual(len(self.cache.node_dict), 3)

        # update item 1, so nothing should get popped
        # but LRU is now item 2
        self.cache.put(1, "updated_node_val_1")
        self.assertEqual(len(self.cache.node_dict), 3)

        self.cache.put(4, "node_val_4")

        item_1 = self.cache.get(1)
        # this should now no longer exist
        item_2 = self.cache.get(2)

        self.assertEqual(len(self.cache.node_dict), 3)
        self.assertIsNotNone(item_1)
        self.assertIsNone(item_2)        


class LRUCacheOrderingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.cache = LRUCache(3)

    def test_put_get_ordering(self):
        # dict is empty to start
        self.assertEqual(len(self.cache.node_dict), 0)

        self.cache.put(1, "node_val_1")
        node_1 = self.cache.get(1)

        self.assertEqual(node_1.next_node.key, self.cache.tail.key)
        self.assertEqual(node_1.next_node.val, self.cache.tail.val)
        self.assertEqual(node_1.prev_node.key, self.cache.head.key)
        self.assertEqual(node_1.prev_node.val, self.cache.head.val)

        self.cache.put(2, "node_val_2")
        node_2 = self.cache.get(2)

        self.cache.put(3, "node_val_3")
        node_3 = self.cache.get(3)

        # order should now be head -> node_1 -> node_2 -> node_3 -> tail
        self.assertEqual(self.cache.head.next_node.key, node_1.key)
        self.assertEqual(node_1.prev_node.key, self.cache.head.key)

        self.assertEqual(node_1.next_node.key, node_2.key)
        self.assertEqual(node_2.prev_node.key, node_1.key)

        self.assertEqual(node_2.next_node.key, node_3.key)
        self.assertEqual(node_3.prev_node.key, node_2.key)

        self.assertEqual(node_3.next_node.key, self.cache.tail.key)
        self.assertEqual(self.cache.tail.prev_node.key, node_3.key)

        # if we get(2), node_2 should get set to the tail 
        node_2 = self.cache.get(2)

        # order should now be head -> node_1 -> node_3 -> node_2 -> tail
        self.assertEqual(self.cache.head.next_node.key, node_1.key)
        self.assertEqual(node_1.prev_node.key, self.cache.head.key)

        self.assertEqual(node_1.next_node.key, node_3.key)
        self.assertEqual(node_3.prev_node.key, node_1.key)

        self.assertEqual(node_3.next_node.key, node_2.key)
        self.assertEqual(node_2.prev_node.key, node_3.key)

        self.assertEqual(node_2.next_node.key, self.cache.tail.key)
        self.assertEqual(self.cache.tail.prev_node.key, node_2.key)

        # if we put(1), node_1 should now get sent to the tail
        self.cache.put(node_1.key, node_1.val)

        # order should now be head -> node_3 -> node_2 -> node_1 -> tail
        self.assertEqual(self.cache.head.next_node.key, node_3.key)
        self.assertEqual(node_3.prev_node.key, self.cache.head.key)

        self.assertEqual(node_3.next_node.key, node_2.key)
        self.assertEqual(node_2.prev_node.key, node_3.key)

        self.assertEqual(node_2.next_node.key, node_1.key)
        self.assertEqual(node_1.prev_node.key, node_2.key)

        self.assertEqual(node_1.next_node.key, self.cache.tail.key)
        self.assertEqual(self.cache.tail.prev_node.key, node_1.key)
