class OrderedStack:
    def __init__(self):
        self.top = -1
        self.stack = []

    def __iter__(self):
        t_top = self.top
        while True:
            if t_top == -1:
                break
            yield self.stack[t_top]
            t_top -= 1

    def __len__(self):
        return self.top + 1

    def size(self):
        return len(self)

    def is_empty(self):
        return self.top == -1

    def push(self, val):
        if self.is_empty():
            self.t_push(val)
        else:
            tmp_stack = OrderedStack()
            while not self.is_empty() and val < self.peek():
                tmp_stack.t_push(self.pop())
            tmp_stack.t_push(val)
            while not tmp_stack.is_empty():
                self.t_push(tmp_stack.pop())

    def t_push(self, val):
        self.stack.append(val)
        self.top += 1

    def pop(self):
        if self.is_empty():
            raise IndexError("stack empty")
        val = self.stack.pop()
        self.top -= 1
        return val

    def peek(self):
        if self.is_empty():
            raise IndexError("stack empty")
        return self.stack[self.top]
