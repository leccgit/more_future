from abc import ABC

from algorithms_python.search_st.abs_st import AbsST


class Node:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.next = None


class SequentialSearchST(AbsST, ABC):
    def __init__(self):
        self._head: Node = None
        self._size = 0

    def get(self, key):
        travel_head = self._head
        while travel_head:
            if travel_head.key == key:
                return travel_head.val
            travel_head = travel_head.next
        return None

    def put(self, key, val):
        travel_head = self._head
        if val is None:
            pre_node = None
            while travel_head:
                if travel_head.key == key:
                    if pre_node:
                        pre_node.next = travel_head.next
                    else:
                        self._head = travel_head.next
                    self._size -= 1
                    return
                pre_node = travel_head
                travel_head = travel_head.next
        else:
            while travel_head:
                if travel_head.key == key:
                    travel_head.val = val
                    return
                travel_head = travel_head.next
            new_node = Node(key, val)
            new_node.next = self._head
            self._head = new_node
            self._size += 1
            return None

    def delete(self, key):
        self.put(key, None)

    def keys(self):
        travel_head = self._head
        while travel_head:
            yield travel_head.key
            travel_head = travel_head.next

    def size(self):
        return self._size

    def is_empty(self) -> bool:
        return self._size == 0

    def contains(self, item) -> bool:
        all_keys = list(self.keys())
        return item in all_keys


class BinarySearchST(AbsST, ABC):
    def __init__(self):
        self._key = []
        self._val = []
        self._size = 0

    def get(self, key):
        if self.is_empty():
            return None
        _key_idx = self._rank(key)
        if _key_idx < self._size and self._key[_key_idx] == key:
            return self._val[_key_idx]
        return None

    def put(self, key, val):
        _key_idx = self._rank(key)
        if val is None:
            if _key_idx < self._size and self._key[_key_idx] == key:
                del self._key[_key_idx]
                del self._val[_key_idx]
                self._size -= 1
                return
        else:

            if _key_idx < self._size and self._key[_key_idx] == key:
                self._val[_key_idx] = val
                return
            self._key.insert(_key_idx, key)
            self._val.insert(_key_idx, val)
            self._size += 1

    def _rank(self, key) -> int:
        lo = 0
        hi = self._size - 1  # 有可能为-1
        while lo <= hi:
            mid = lo + (hi - lo) // 2
            if str(self._key[mid]) < str(key):
                lo = mid + 1
            elif str(self._key[mid]) > str(key):
                hi = mid - 1
            else:
                return mid
        return lo

    def delete(self, key):
        self.put(key, None)

    def keys(self):
        for key in self._key:
            yield key

    def size(self):
        return self._size

    def is_empty(self) -> bool:
        return self.size() == 0

    def contains(self, item) -> bool:
        return item in self.keys()
