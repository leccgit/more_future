# -*- coding:utf-8 -*-
import os


def is_all_chinese(raw_str: str) -> bool:
    # 校验是否全中文
    for _char in raw_str:
        if not '\u4e00' <= _char <= '\u9fa5':
            return False
    return True


def check_file(file_name):
    # 校验文件是否存在
    if not file_name.endswith("txt"):
        file_name = "{}.txt".format(file_name)
    if not os.path.isfile(file_name):
        raise FileExistsError("{}, 不存在!".format(file_name))
    return file_name


def re_write_file():
    input_file = input("请输入原始文档路径: ")
    check_file(input_file)
    output_file = input("请输入文档保存路径: ")
    check_file(output_file)
    with open(output_file, "a") as f:
        with open(input_file, "r") as raw_f:
            for one_line in raw_f.readlines():
                if is_all_chinese(one_line.strip("\n")):
                    f.writelines(one_line)
    print("文件处理完毕...")


if __name__ == '__main__':
    re_write_file()
