from werkzeug.local import LocalStack, LocalProxy


def with_out_local_proxy():
    l_stack = LocalStack()
    l_stack.push({'name': 'ayuliao'})
    l_stack.push({'name': 'twotwo'})

    def get_name():
        return l_stack.pop()

    name = get_name()
    print(f"name is {name['name']}")
    print(f"name is {name['name']}")


def with_local_proxy():
    l_stack = LocalStack()
    l_stack.push({'name': 'ayuliao'})
    l_stack.push({'name': 'twotwo'})

    def get_name():
        return l_stack.pop()

    name = LocalProxy(get_name)
    print(f"name is {name['name']}")
    print(f"name is {name['name']}")


with_out_local_proxy()
with_local_proxy()



