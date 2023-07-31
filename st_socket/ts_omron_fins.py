from socket import socket

if __name__ == '__main__':
    for _ in range(10):
        socket_client = socket()
        socket_client.settimeout(1000 / 1000)
        socket_client.connect(('192.168.32.226', 9600))
        fins_command = b'\x46\x49\x4E\x53\x00\x00\x00\x0C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

        socket_client.sendall(fins_command)
        # time.sleep(0.5)
        t_result = socket_client.recv(24)
        print(t_result)

        s = b'FINS\x00\x00\x00\x10\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\xe2\x00\x00\x00\x06'
        s = b'FINS\x00\x00\x00\x10\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x06'
        # fins_sa1 = s[19]
        # fins_da1 = s[23]
        # print(fins_sa1, fins_da1)
        if t_result[15] != 0:
            print(f'omron init node fail, '
                  f'NASD command error recv_content[15]:{t_result[15]}.')
        if t_result[8] != 0 or t_result[9] != 0 or t_result[10] != 0 or t_result[11] != 1:
            error_list = [t_result[8], t_result[9], t_result[10], t_result[11]]
            print(f'omron init node fail, '
                  f'Error sending NADS command respNADS[8]...respNADS[11]:{error_list}')

        print(t_result[19], t_result[23])
        # time.sleep(0.5)
