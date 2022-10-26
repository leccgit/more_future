"""
Stack Abstract Data Type (ADT)
"""
from abc import ABC, ABCMeta, abstractmethod


class AbstractStack(metaclass=ABCMeta):
    """Abstract Class for Stacks."""

    def __init__(self):
        self._top = -1

    def __len__(self):
        return self._top + 1

    def __str__(self):
        result = " ".join(map(str, self))
        return 'Top-> ' + result

    def is_empty(self):
        return self._top == -1

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def push(self, value):
        pass

    @abstractmethod
    def pop(self):
        pass

    @abstractmethod
    def peek(self):
        pass


class ArrayStack(AbstractStack):
    def __init__(self, size: int = 10):
        super(ArrayStack, self).__init__()
        self._stack: list = [None] * size

    def __iter__(self):
        st_idx = self._top
        while True:
            if st_idx == -1:
                break
            yield self._stack[st_idx]
            st_idx -= 1

    def push(self, value):
        self._top += 1
        if self._top == len(self._stack):
            self._expand()
        self._stack[self._top] = value

    def pop(self):
        if self.is_empty():
            raise IndexError("ArrayStack empty!")
        val = self._stack[self._top]
        self._stack[self._top] = None  # 清除当前栈的元素
        self._top -= 1
        return val

    def peek(self):
        # 返回栈顶元素
        if self.is_empty():
            raise IndexError("ArrayStack empty!")
        return self._stack[self._top]

    def _expand(self):
        # 扩容
        self._stack += [None] * len(self._stack)


class Node(object):
    def __init__(self, val):
        self.val = val
        self.next = None


class LinkedListStack(AbstractStack, ABC):
    # 使用单链表构建的栈，头插法
    def __init__(self):
        super(LinkedListStack, self).__init__()
        self._head: Node = None

    def __iter__(self):
        st_head = self._head
        while st_head:
            yield st_head.val
            st_head = st_head.next

    def push(self, value):
        node = Node(value)
        # if self._head:
        #     node.next = self._head
        node.next = self._head
        self._head = node
        self._top += 1

    def pop(self):
        if self.is_empty():
            raise IndexError("LinkedListStack empty")
        val = self._head.val
        self._head = self._head.next
        self._top -= 1
        return val

    def peek(self):
        if self.is_empty():
            raise IndexError("LinkedListStack empty")
        return self._head.val
