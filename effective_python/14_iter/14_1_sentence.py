import re
import reprlib

RE_WORD = re.compile("\w+")


class Sentence:
    def __init__(self, text: str):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __getitem__(self, idx: int):  # 序列类型
        return self.words[idx]

    def __len__(self):
        return len(self.words)

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)  # reprlib.repr用于生成大型数据结构的简略字符串表现形式


if __name__ == '__main__':
    s = Sentence('"The time has come," the Walrus said,')
    print(s)
    for word in s:
        print(word)
