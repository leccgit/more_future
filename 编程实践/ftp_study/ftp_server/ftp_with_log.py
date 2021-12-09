import logging

from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer

authorizer = DummyAuthorizer()
authorizer.add_user('user', '12345', '.', perm='elradfmwMT')
handler = FTPHandler
handler.authorizer = authorizer

logging.basicConfig(filename='/var/log/pyftpd.log', level=logging.INFO)

server = FTPServer(('', 2121), handler)
server.serve_forever()