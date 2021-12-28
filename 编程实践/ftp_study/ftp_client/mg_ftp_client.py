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


def build_ftp_conn_params(
        host="", port=21, user="", passwd="", timeout=10
) -> FtpConnParams:
    conn_params = FtpConnParams()
    conn_params.host = host
    conn_params.port = int(port)
    conn_params.user = user
    conn_params.passwd = passwd
    conn_params.timeout = int(timeout)

    return conn_params


def build_ftp_connection(
        ftp_client: FTP,
        conn_params: FtpConnParams
) -> FTP:
    # 构建ftp连接参数
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
    # 校验指定文件名，在远端的ftp服务器中是否存在
    try:
        if file_name in ftp_client.nlst(ftp_path):
            return True
        else:
            return False
    except error_perm:
        return False


def ftp_down_load_file(
        conn_params: FtpConnParams,
        ftp_file: str,
        local_file: str = "",
        buf_size=1024
) -> None:
    """
    通过ftp读取远端的文件，并保存到本地
    :param conn_params:
    :param ftp_file: 远程文件路径
    :param local_file: 本地文件路径
    :param buf_size: 单次读取文件buf, 默认1kb
    :return:
    """
    # 构建文件参数
    ftp_file_name = os.path.basename(ftp_file)
    ftp_file_dir = os.path.dirname(ftp_file)
    if not local_file:
        local_file_name = ftp_file_name
    else:
        local_file_name = os.path.basename(local_file)
    local_file_path = os.path.join(os.path.dirname(__file__), local_file_name)

    # 创建连接参数
    with FTP() as ftp_client:
        # 建立ftp客户端的连接
        build_ftp_connection(ftp_client, conn_params)
        # 校验远端的文件是否存在
        if not is_ftp_file(ftp_client, ftp_file_name, ftp_file_dir):
            raise FtpFileNotFound("ftp file not found,"
                                  " file:{} not exits!".format(ftp_file))
        # 读取文件保存到本地
        with open(local_file_path, "wb") as f:
            ftp_client.retrbinary(
                'RETR %s' % ftp_file, f.write, buf_size)
    print("down load suc......")


if __name__ == '__main__':
    pass
