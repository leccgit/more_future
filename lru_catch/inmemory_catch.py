import time
from threading import RLock
from typing import Dict, Iterator

SET_FAIL = None


class Node:
    def __init__(self, data, ttl_ts: int = None):
        self.data = data
        if ttl_ts is None:
            ttl_ts = float('inf')
        self.ttl_ts = ttl_ts


class InMemoryCatch:
    _store: Dict[str, Node] = {}
    _set_times = 0
    _lock = RLock()

    @property
    def _now(self) -> int:
        return int(time.time())

    def _get(self, key: str):
        v = self._store.get(key)
        if v:
            if v.ttl_ts <= self._now:
                del self._store[key]
            else:
                return v

    def get(self, key: str) -> str:
        with self._lock:
            v = self._get(key)
            if v:
                return v.data

    def set(self, key: str, value: str, expire: int = None, nx=False, xx=False):
        if not key or not value:
            raise ValueError("please check, can't set empty key or value.")
        if all([nx, xx]):
            raise ValueError("please check, nx and xx can't set together.")

        if nx and self.get(key):
            return SET_FAIL
        if xx and not self.get(key):
            return SET_FAIL

        when_expire = None
        if expire:
            when_expire = self._now + expire

        with self._lock:
            self._store[key] = Node(value, when_expire)
            self._set_times += 1
        self._clear_expire()
        return value

    def _clear_expire(self):
        if self._set_times % 100 == 0:
            keys = list(self._store.keys())
            for key in keys:
                self._get(key)

    def scan(self) -> Iterator:
        for key in list(self._store.keys()):
            val = self.get(key)
            if val:
                yield key, val


if __name__ == '__main__':
    in_memory = InMemoryCatch()
    in_memory.set("name", "lei")
    assert in_memory.get("name") == "lei"
    if in_memory.set("name", "lei", nx=True):
        print("nx set fail, key already exist.")
    if in_memory.set("name", "lei", xx=True):
        print("nx set suc, key already exist.")
    for key, val in in_memory.scan():
        print(key, val)
