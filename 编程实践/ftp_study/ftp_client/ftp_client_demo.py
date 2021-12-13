import os
from ftplib import FTP, error_perm


class FtpFileNotFound(Exception):
    pass


class FtpConnParams:
    # 构建ftp的连接参数
    def __init__(self):
        self.host = ""
        self.port = 21
        self.user = ""
        self.passwd = ""
        self.timeout = 10


def create_ftp_conn_params(
        host="", port=21, user="", passwd="", timeout=10
) -> FtpConnParams:
    conn_params = FtpConnParams()
    conn_params.host = host
    conn_params.port = int(port)
    conn_params.user = user
    conn_params.passwd = passwd
    conn_params.timeout = int(timeout)

    return conn_params


def create_ftp_connection(
        ftp_client: FTP,
        conn_params: FtpConnParams
) -> FTP:
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
        file_name: str,
        ftp_path: str
) -> bool:
    """
    校验当前文件, 是否存在于远端的ftp服务器的指定文件目录下
    :param ftp_client:
    :param file_name: 检查的ftp文件名称
    :param ftp_path: 校验的ftp文件路径
    :return:
    """
    try:
        if file_name in ftp_client.nlst(ftp_path):
            return True
        else:
            return False
    except error_perm:
        return False


def ftp_down_load_file(
        conn_params: FtpConnParams,
        remote_file: str,
        local_file: str = "",
        buf_size=1024
):
    """
    通过ftp读取远端的文件，并保存到本地
    :param conn_params:
    :param remote_file: 远程文件路径
    :param local_file: 保存的本地文件路径
    :param buf_size: 一次读取的文件Buf大小
    :return:
    """
    # 构建文件参数
    ftp_file = os.path.basename(remote_file)
    ftp_file_path = os.path.dirname(remote_file)
    if not local_file:
        local_file_name = ftp_file
    else:
        local_file_name = os.path.basename(local_file)
    save_local_file = os.path.join(os.path.dirname(__file__), local_file_name)

    # 创建连接参数
    with FTP() as ftp_client:
        # 建立ftp客户端的连接
        create_ftp_connection(ftp_client, conn_params)
        # 校验远端的文件是否存在
        if not is_ftp_file(ftp_client, ftp_file, ftp_file_path):
            raise FtpFileNotFound("ftp file not fount,"
                                  " file:{} not exits!".format(remote_file))
        # 读取文件保存到本地
        with open(save_local_file, "wb") as f:
            ftp_client.retrbinary(
                'RETR %s' % remote_file, f.write, buf_size)
    print("down load suc......")


if __name__ == '__main__':
    pass