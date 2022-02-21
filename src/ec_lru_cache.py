from typing import Any, Optional


class Node:
    """
    Item the doubly linked list
    """
    def __init__(self, key: int, val: Any) -> None:
        self.key = key
        self.val = val
        self.prev_node = None
        self.next_node = None


class LRUCache:
    """
    Base of the cache. Once instantiated, items can be added to the cache via `put()`
    and retrieved from the cache via `get()`. Items' values can also be updated with `put()`.
    
    Any interaction with an item in the cache (i.e. `put()` or `get()`)
    puts that item at the "end" of the cache list, thus making it the most recently used
    item and the furthest away from being popped.
    
    Once the `capacity` limit is reached, the least recently used item will be removed from the cache.
    Default value for the `capacity` is 100.
    """
    def __init__(self, capacity: int = 100) -> None:
        self.capacity = capacity
        self.node_dict = {}

        # Setup dummy head & tail nodes of the linked list to simplify adding/removing/updating
        self.head = Node(0, "head")
        self.tail = Node(0, "tail")
        self.head.next_node = self.tail
        self.tail.prev_node = self.head

    def get(self, key: int) -> Optional[Node]:
        """
        Get Node based on `key`. If the Node doesn't exist, will return `None`.
        """
        if node := self.node_dict.get(key):
            self._update_node(node)

            return node

        return None

    def put(self, key: int, value: Any) -> None:
        """
        Creates a new item in the cache based on key & any sort of value. Can later be accessed
        """
        if node := self.node_dict.get(key):
            # we only need to update the node in the linked list
            self._update_node(node)
            node.val = value
        else:
            # we need to check if we hit the cap, then add the new node
            if len(self.node_dict) >= self.capacity:
                self._pop_head_node()

            node = Node(key, value)
            self._add_node(node)

        self.node_dict[key] = node

    def _update_node(self, node: Node) -> None:
        self._remove_node(node)
        self._add_node(node)

    def _add_node(self, node: Node) -> None:
        """
        Add `node` to the doubly linked list. Adds it to the
        end (tail) of the list, and shifts all existing instances
        forward one step towards the head.
        """
        current_tail_node = self.tail.prev_node
        current_tail_node.next_node = node

        self.tail.prev_node = node
        node.prev_node = current_tail_node
        node.next_node = self.tail

    def _remove_node(self, node: Node) -> None:
        """
        Remove `node` from the doubly linked list by updating it's
        prev_node and next_node underlying objects to the new proper values
        """
        prev_node = node.prev_node
        next_node = node.next_node

        prev_node.next_node = next_node
        next_node.prev_node = prev_node

    def _pop_head_node(self) -> None:
        """
        Removes the head (aka the least recently used) node
        from the linked list and from the dict
        """
        node_to_remove = self.head.next_node
        self._remove_node(node_to_remove)
        self.node_dict.pop(node_to_remove.key)
