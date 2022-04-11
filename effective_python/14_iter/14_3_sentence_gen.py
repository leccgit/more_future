import re
import reprlib

RE_WORD = re.compile("\w+")


class Sentence:
    def __init__(self, text: str):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

    def __len__(self):
        return len(self.words)

    def __iter__(self):
        for w in self.words:
            yield w


if __name__ == '__main__':
    s = Sentence('"The time has come," the Walrus said,')
    print(s)
    for word in s:
        print(word)
