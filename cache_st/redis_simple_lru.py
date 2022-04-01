from datetime import datetime, timedelta


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.when_expire = None

    def __repr__(self):
        return str({
            "key": self.key,
            "value": self.value,
        })


def create_node(
        key: str, value,
) -> Node:
    # 创建一个node节点, 该节点不会过期
    return Node(key=key, value=value)


def set_node_when_expire(
        node: Node, when_expire: datetime,
) -> Node:
    # 设置节点的过期时间
    node.when_expire = when_expire
    return node


def node_is_expired(node: Node) -> bool:
    # 校验当前的node节点是否过期
    if not node:
        return False
    when_expire = node.when_expire
    if not when_expire:
        return False
    return when_expire < datetime.now()


class KeySpace:
    def __init__(self):
        self.key_space = {}

    def _expire_if_need(self, key):
        node = self.key_space.get(key)
        if not node_is_expired(node):
            return
        del self.key_space[key]
        print("key:{} is expire".format(key))

    def _look_up_key(self, key) -> Node or Node:
        return self.key_space.get(key) or None

    def get_generic_key(self, key):
        self._expire_if_need(key)
        node = self._look_up_key(key)
        return node.value if node else None

    def set_generic_key(self, key, value, expire_seconds: int = 0):
        when_expire = None
        if expire_seconds:
            when_expire = datetime.now() + timedelta(seconds=expire_seconds)
        node = create_node(key, value)
        if when_expire:
            set_node_when_expire(node, when_expire)
        self.key_space[key] = node

    def lookup_all_keys(self):
        result = {}
        for key in list(self.key_space.keys()):
            value = self.get_generic_key(key)
            if key in self.key_space:
                result[key] = value
        return result

    def __repr__(self):
        return str(self.lookup_all_keys())


if __name__ == '__main__':
    import time

    key_space = KeySpace()
    key_space.set_generic_key("name", "leichao", expire_seconds=2)
    for i in range(10):
        time.sleep(.3)
        print(key_space)
