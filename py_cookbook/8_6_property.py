class Person:
    def __init__(self, first_name):
        self.first_name = first_name  # ps: 该处first_name, 已经调用@first_name.setter方法, 而非普通的实例属性

    # Getter function
    @property
    def first_name(self):
        return self._first_name

    # Setter function
    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._first_name = value

    # Deleter function (optional)
    @first_name.deleter
    def first_name(self):
        raise AttributeError("Can't delete attribute")


if __name__ == '__main__':
    t_p = Person(23)
    print(t_p.first_name)
