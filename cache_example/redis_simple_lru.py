from collections import OrderedDict
from datetime import datetime, timedelta

_KEY_SPACE = OrderedDict()


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.when_expire = None

    def __repr__(self):
        return "<{}:{}, when_expire:{}>".format(
            self.key, self.value, self.when_expire)


def create_node(
        key: str, value,
) -> Node:
    # 创建一个永不过期的node节点
    return Node(key=key, value=value)


def set_node_when_expire(
        node: Node,
        when_expire: datetime = None,
) -> Node:
    # 设置节点过期时间
    node.when_expire = when_expire
    return node


def node_is_expired(node: Node) -> bool:
    # 校验当前节点是否过期
    if not node or not node.when_expire:
        return False
    return node.when_expire < datetime.now()


class ExpireDict:
    def __init__(self):
        self.key_space = _KEY_SPACE

    @staticmethod
    def _expire_if_need(db_obj: dict, key):
        node = db_obj.get(key, None)
        if not node_is_expired(node):
            return
        del db_obj[key]
        print("key:{} expire".format(key))

    @staticmethod
    def _look_up_key(db_obj: dict, key) -> Node or None:
        return db_obj.get(key) or None

    def get_generic_key(self, db_key: str, key: str):
        db_obj = self.key_space.get(db_key, {})
        if not db_obj:
            return
        self._expire_if_need(db_obj, key)
        node = self._look_up_key(db_obj, key)
        return node.value if node else None

    def set_generic_key(self, db_key: str, key: str, value, expire_seconds: int = 0):
        db_obj = self.key_space.setdefault(db_key, {})

        node = create_node(key, value)
        if expire_seconds:
            when_expire = datetime.now() + timedelta(seconds=expire_seconds)
            set_node_when_expire(node, when_expire)
        db_obj[key] = node


def get_generic_key(db_key: str, key: str):
    return ExpireDict().get_generic_key(db_key, key)


def set_generic_key(db_key: str, key: str, value, expire_seconds: int = 0):
    return ExpireDict().set_generic_key(db_key, key, value, expire_seconds)


if __name__ == '__main__':
    import time

    set_generic_key("test", "name", "leichao", expire_seconds=2)

    for i in range(10):
        print(get_generic_key("test", "name"))

        time.sleep(.3)
    print(_KEY_SPACE)
