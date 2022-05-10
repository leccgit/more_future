import unittest

from algorithms_with_python.stack.ordered_stack import OrderedStack
from algorithms_with_python.stack.stack import ArrayStack, LinkedListStack


class TestStack(unittest.TestCase):
    def test_ArrayStack(self):
        stack = ArrayStack()
        stack.push(1)
        stack.push(2)
        stack.push(3)
        print(stack)

        # test __iter__()
        it = iter(stack)
        self.assertEqual(3, next(it))
        self.assertEqual(2, next(it))
        self.assertEqual(1, next(it))
        self.assertRaises(StopIteration, next, it)

        # test __len__()
        self.assertEqual(3, len(stack))

        # test __str__()
        self.assertEqual(str(stack), "Top-> 3 2 1")

        # test is_empty()
        self.assertFalse(stack.is_empty())

        # test peek()
        self.assertEqual(3, stack.peek())

        # test pop()
        self.assertEqual(3, stack.pop())
        self.assertEqual(2, stack.pop())
        self.assertEqual(1, stack.pop())

        self.assertTrue(stack.is_empty())

    def test_LinkedListStack(self):
        stack = LinkedListStack()

        stack.push(1)
        stack.push(2)
        stack.push(3)
        # test __iter__()
        it = iter(stack)
        self.assertEqual(3, next(it))
        self.assertEqual(2, next(it))
        self.assertEqual(1, next(it))
        self.assertRaises(StopIteration, next, it)

        # test __len__()
        self.assertEqual(3, len(stack))

        # test __str__()
        self.assertEqual(str(stack), "Top-> 3 2 1")

        # test is_empty()
        self.assertFalse(stack.is_empty())

        # test peek()
        self.assertEqual(3, stack.peek())

        # test pop()
        self.assertEqual(3, stack.pop())
        self.assertEqual(2, stack.pop())
        self.assertEqual(1, stack.pop())

        self.assertTrue(stack.is_empty())


class TestOrderedStack(unittest.TestCase):
    def test_OrderedStack(self):
        stack = OrderedStack()
        self.assertTrue(stack.is_empty())
        stack.push(1)
        stack.push(4)
        stack.push(3)
        stack.push(6)
        "bottom - > 1 3 4 6 "
        self.assertEqual(6, stack.pop())
        self.assertEqual(4, stack.peek())
        self.assertEqual(3, stack.size())


if __name__ == '__main__':
    unittest.main()
