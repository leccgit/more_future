import re
from collections import defaultdict

"""
 'Python官网的网址是https://www.python.org/ dfsafda'
 lei
 chao
 127.02.3
  'Python官网的网址是https://www.python.org/ dfsafda'
 'Python官网的网址是https://www.python.org/ dfsafda'
 'Python官网的网址是https://www.python.org/ dfsafda'
 'Python官网的网址是https://www.python.org/ dfsafda'
 'Python官网的网址是https://www.python.org/ dfsafda'
 'Python官网的网址是https://www.pythonss.org/ dfsafda'


 'Python官网的网址是https://www.pythonss.org/ dfsafda'
 'Python官网的网址是https://www.pythonss.org/ dfsafda'
 'Python官网的网址是https://www.pythonss.org/ dfsafda'
"""
re_pattern = re.compile(r"(?:(?:http:\/\/)|(?:https:\/\/))?(?:[\w](?:[\w\-]{0,61}[\w])?\.)+[a-zA-Z]{2,6}(?:\/)")


def read_domain(file_name: str) -> dict:
    assert file_name, "文件名称不能为空！"
    with open(file_name, "r") as f:
        result = defaultdict(int)
        for rc in re_pattern.findall(f.read()):
            result[rc] += 1
        return result


if __name__ == '__main__':
    print(read_domain("./file_name"))
