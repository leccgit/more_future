from abc import ABC
from typing import List

from algorithms_with_python.search_st.abs_st import AbsST


def key_hash(key):
    return hash(key)


class Node:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.next = None


class ArrayHashST(AbsST, ABC):
    def __init__(self):
        self._size = 0
        self._mask: int = 16
        self._items: List[Node] = [None] * self._mask

    def put(self, key, val):
        if key is None:
            raise KeyError("put key not be None!")
        key_idx = self._key_idx(key)
        _key_node = self._items[key_idx]
        if val is None:
            # 针对key的删除操作
            if not _key_node:
                return None
            pre_node = None
            while _key_node:
                if _key_node.key == key:
                    if pre_node:
                        pre_node.next = _key_node.next
                    else:
                        self._items[key_idx] = _key_node.next
                    self._size -= 1
                    return
                pre_node = _key_node
                _key_node = _key_node.next
        else:
            while _key_node:
                if _key_node.key == key:
                    _key_node.val = val
                    return
                _key_node = _key_node.next
            new_node = Node(key, val)
            new_node.next = self._items[key_idx]
            self._items[key_idx] = new_node
            self._size += 1

    def get(self, key):
        if key is None:
            raise KeyError("get key not be None!")
        key_idx = self._key_idx(key)
        key_node = self._items[key_idx]
        while key_node:
            if key_node.key == key:
                return key_node.val
            key_node = key_node.next
        return None

    def delete(self, key):
        self.put(key, None)

    def keys(self):
        for i in range(self._mask):
            _tmp_node = self._items[i]
            while _tmp_node:
                yield _tmp_node.key
                _tmp_node = _tmp_node.next

    def size(self):
        return self._size

    def is_empty(self) -> bool:
        return bool(self._size)

    def contains(self, key) -> bool:
        all_keys = list(self.keys())
        return key in all_keys

    def _key_idx(self, key):
        return key_hash(key) % self._mask
