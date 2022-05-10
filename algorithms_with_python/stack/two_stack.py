class StackError(Exception):
    pass


class Stack:
    def __init__(self, max_len: int):
        self.max_len = max_len
        self.top0 = -1
        self.top1 = max_len
        self.stack = ["None"] * max_len

    def empty(self) -> bool:
        return self.top0 == -1 and self.top1 == self.max_len

    def full(self) -> bool:
        return self.top0 + 1 >= self.top1

    def __repr__(self):
        return str(self.stack)


def stack_push(d_stack: Stack, element, flag: str = "1"):
    if d_stack.full():
        raise StackError("stack full")
    if flag == "1":
        d_stack.top0 += 1
        d_stack.stack[d_stack.top0] = element
    else:
        d_stack.top1 -= 1
        d_stack.stack[d_stack.top1] = element


def stack_pop(d_stack: Stack, flag: str = "1"):
    if d_stack.empty():
        raise StackError("stack empty")
    if flag == "1":
        if d_stack.top0 == -1:
            raise StackError("stack_top0 empty")
        else:
            d_stack.stack[d_stack.top0] = "None"
            d_stack.top0 -= 1
    else:
        if d_stack.top1 == d_stack.max_len:
            raise StackError("stack_top1 empty")
        else:
            d_stack.stack[d_stack.top1] = "None"
            d_stack.top1 += 1


if __name__ == '__main__':
    stack_a = Stack(max_len=9)
    stack_push(stack_a, 2)
    stack_push(stack_a, 3)
    stack_push(stack_a, 4)

    stack_push(stack_a, 2, flag="2")
    stack_push(stack_a, 3, flag="2")
    stack_push(stack_a, 4, flag="2")
    stack_push(stack_a, 5, flag="2")
    stack_push(stack_a, 6, flag="2")
    stack_push(stack_a, 7, flag="2")
    stack_pop(stack_a, flag="1")

    print(stack_a)
    stack_push(stack_a, 8, flag="1")
