class RecordCollection(object):
    """A set of excellent Records from a query."""

    def __init__(self, rows):
        self._rows = rows
        self._all_rows = []
        self.pending = True

    def __repr__(self):
        return '<RecordCollection size={} pending={}>'.format(len(self), self.pending)

    def __iter__(self):
        """行遍历的时候，只有在需要的时候调用next(self)，同时将生成器中的元素添加到缓存列表中，避免后续迭代iter资源被耗尽问题"""
        i = 0
        while True:
            # Other code may have iterated between yields,
            # so always check the cache.
            if i < len(self):
                yield self[i]  # __getitem__
            else:
                # Throws StopIteration when done.
                # Prevent StopIteration bubbling from generator, following https://www.python.org/dev/peps/pep-0479/
                try:
                    yield next(self)  # __next__
                except StopIteration:
                    return
            i += 1

    def __next__(self):
        try:
            next_row = next(self._rows)
            self._all_rows.append(next_row)
            return next_row
        except StopIteration:
            self.pending = False
            raise StopIteration('RecordCollection contains no more rows.')

    def __getitem__(self, key):
        is_int = isinstance(key, int)

        # Convert RecordCollection[1] into slice.
        if is_int:
            key = slice(key, key + 1)  # 该处将key转换为切片

        while len(self) < key.stop or key.stop is None:
            try:
                next(self)
            except StopIteration:
                break

        rows = self._all_rows[key]
        if is_int:
            return rows[0]
        else:
            return RecordCollection(iter(rows))

    def __len__(self):  # ps: 该处的使用存在bug, 如果没有对RecordCollection进行完整的迭代，那么len(self._all_rows) != self._rows
        return len(self._all_rows)


if __name__ == '__main__':
    from collections import namedtuple

    IdRecord = namedtuple('IdRecord', 'id')

    records = RecordCollection(IdRecord(i) for i in range(10))
    print(len(records))
    print(records[5])
    # for rc in records:
    #     print(rc)
    # for rc in records:
    #     print(rc)
