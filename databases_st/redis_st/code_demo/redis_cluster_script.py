import subprocess


def get_process_id(name: str) -> list:
    """
    根据服务名称，获取运行程序的pid
    :param name: 程序服务名称
    :return:
    """
    child = subprocess.Popen(['pgrep', '-f', name], stdout=subprocess.PIPE, shell=False)
    response = child.communicate()[0]
    return [int(pid) for pid in response.split()]


if __name__ == '__main__':
    print(get_process_id("python"))
