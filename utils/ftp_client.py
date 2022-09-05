import os
import time
from ftplib import FTP, error_perm
from typing import Tuple


class FtpFileNotFound(Exception):
    pass


class FtpConnParams:
    # ftp的连接参数
    def __init__(self):
        self.host = ""
        self.port = 21
        self.user = ""
        self.passwd = ""
        self.timeout = 10


def build_ftp_conn_params(
        host="", port=21, user="", passwd="", timeout=10
) -> FtpConnParams:
    assert host, "ftp host is None!"

    # 构建ftp的连接参数
    conn_params = FtpConnParams()
    conn_params.host = host
    conn_params.port = int(port)
    conn_params.user = user
    conn_params.passwd = passwd
    conn_params.timeout = int(timeout)

    return conn_params


def create_ftp_conn_params(
        ftp_client: FTP,
        conn_params: FtpConnParams
) -> FTP:
    # 建立ftp连接
    ftp_client.connect(
        host=conn_params.host,
        port=conn_params.port,
        timeout=conn_params.timeout,
    )
    ftp_client.login(
        user=conn_params.user,
        passwd=conn_params.passwd
    )
    return ftp_client


def is_ftp_file(
        ftp_client: FTP,
        remote_file: str,
) -> bool:
    # 校验指定文件名，在远端的ftp服务器中是否存在
    file_name = os.path.basename(remote_file)
    ftp_path = os.path.dirname(remote_file)
    try:
        if file_name in ftp_client.nlst(ftp_path):
            return True
        else:
            return False
    except error_perm:
        return False


def ftp_download_remote_file_with_time(
        conn_params: FtpConnParams,
        remote_file: str,
        local_file: str = "",
        buf_size=1024,
        time_out=10
) -> Tuple[bool, str]:
    start_time = time.time()
    save_local_file = ftp_download_remote_file(
        conn_params, remote_file, local_file=local_file, buf_size=buf_size)
    end_time = time.time()
    if end_time - start_time > time_out:
        return True, save_local_file
    return False, save_local_file


def ftp_download_remote_file(
        conn_params: FtpConnParams,
        remote_file: str,
        local_file: str = "",
        buf_size=1024
) -> str:
    """
    通过ftp读取远端的文件，并保存到本地
    :param conn_params:
    :param remote_file: 远程文件路径
    :param local_file: 本地文件路径, 默认为空, 将文件保存到当前文件夹下
    :param buf_size: 单次读取文件buf, 默认1kb
    :return:
    """
    assert type(conn_params) is FtpConnParams, "conn_params type error!"
    if not local_file:
        local_file = os.path.join(os.path.dirname(__file__), os.path.basename(remote_file))
    # 创建连接参数
    with FTP() as fp:
        create_ftp_conn_params(fp, conn_params)
        # 校验远端的文件是否存在
        if not is_ftp_file(fp, remote_file):
            raise FtpFileNotFound("ftp file not found, filename:{}".format(remote_file))
        # 读取文件保存到本地
        with open(local_file, "wb") as f:
            fp.retrbinary(
                'RETR %s' % remote_file, f.write, buf_size)
    print("down load suc......")
    print("download file path: {}".format(local_file))
    return local_file


if __name__ == '__main__':
    save_local_path = ftp_download_remote_file_with_time(
        build_ftp_conn_params(
            host="xxxx",
            user="xxx",
            passwd="xxxx"
        ), remote_file=r"is_test/test.mdb")
