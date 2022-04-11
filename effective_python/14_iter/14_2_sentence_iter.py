import re
import reprlib

RE_WORD = re.compile("\w+")


class SentenceIterator:
    # 迭代器
    def __init__(self, words: list):
        self._idx = 0
        self.words = words

    def __iter__(self):
        return self

    def __next__(self):
        try:
            result = self.words[self._idx]
        except IndexError:
            raise StopIteration from None
        self._idx += 1
        return result


class Sentence:
    # 可迭代对象，非迭代器
    def __init__(self, text: str):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)  # reprlib.repr用于生成大型数据结构的简略字符串表现形式

    def __iter__(self):
        return SentenceIterator(self.words)


if __name__ == '__main__':
    s = Sentence('"The time has come," the Walrus said,')
    print(s)
    for word in s:
        print(word)
