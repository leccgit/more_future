from scp import SCPClient
from paramiko import SSHClient, AutoAddPolicy


class MySSHClient:
    def __init__(self, host, port=22, username="", password=""):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

        self.ssh_client = None
        self.scp_client = None

    def __enter__(self):
        self.ssh_client = SSHClient()
        self.ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        self.ssh_client.connect(
            self.host,
            port=self.port,
            username=self.username,
            password=self.password
        )
        self.scp_client = SCPClient(self.ssh_client.get_transport())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.ssh_client.close()
            self.ssh_client = None
            self.scp_client.close()
            self.ssh_client = None
        except Exception as e:
            print("host:{} 关闭连接异常, 请进行核查...... error:{}".format(self.host, str(e)))


def upload_file_with_ssh_by_scp(
        local_path, remote_path,
        host, port=22, username="", password="", exec_command=""):
    """
    通过ssh的方式上传文件
    :param local_path: 本地上传的文件路径, 绝对路径(可以为文件夹)
    :param remote_path: 远程保存的文件路径, 绝对路径
    :param host: 机器ip
    :param port: ssh端口, 默认22
    :param username: 登陆用户名
    :param password: 登陆密码
    :param exec_command: 执行操作
        ex:
            "cd"
    :return:
    """
    with MySSHClient(host, port=port, username=username, password=password) as client:
        client.scp_client.put(local_path, remote_path, recursive=True)
        print("{}: 上传文件成功...".format(host))
        if exec_command:
            std_in, std_out, srd_err = client.ssh_client.exec_command(exec_command)
            print("命令执行错误信息：{}".format(str(srd_err.readlines())))
            print(std_out.read().decode())


def download_file_with_ssh_by_scp(
        remote_path, host, port=22, username="", password=""):
    """
    下载远程ssh连接机器文件到本地
    :param remote_path: 远程文件路径, 绝对路径
    :param host: 机器ip
    :param port: ssh端口, 默认22
    :param username: 登陆用户名
    :param password: 登陆密码
    :return:
    """
    with MySSHClient(host, port=port, username=username, password=password) as client:
        client.scp_client.get(remote_path, recursive=True)
        print("{}: 下载文件成功...".format(host))


if __name__ == '__main__':
    upload_file_with_ssh_by_scp("/study/more_future/code_demo/scp_st/test_1_1.text",
                                "/root/xx/xx/xxx.0.1/log",
                                host="", username="", password="",
                                exec_command="ls -al")
