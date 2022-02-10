from threading import get_ident

from werkzeug.local import LocalStack

ls = LocalStack()
ls.push(42)
print(ls.top)
ls.push(23)
print(ls.top)
print(ls.pop())
print(ls.top)
# for _ in range(10):
#     print(get_ident())
