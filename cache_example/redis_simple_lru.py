from datetime import datetime, timedelta


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.when_expire = None

    def __repr__(self):
        return "{}:{}".format(self.key, self.value)


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


class ExpireDict:
    def __init__(self, key_space: dict = None):
        if key_space is None:
            key_space = {}
        self.key_space = key_space

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


if __name__ == '__main__':
    import time

    simple_test = {"test": {}}
    key_dict = ExpireDict(simple_test["test"])
    key_dict.set_generic_key("name", "leichao", expire_seconds=2)
    for i in range(10):
        print(key_dict.get_generic_key("name"))
        time.sleep(.3)
        print(simple_test)
    print(simple_test)
