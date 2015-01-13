import sockets
import threading

import holepunch.config
import holepunch.request


#class Client:
#
#    def __init__(self, server, conn, addr):
#        self._server = server
#        self._conn = conn
#        self._addr = addr
#
#    def open(self):
#        pass
#
#    def close(self):
#        self._conn.shutdown(socket.SHUT_RDWR)
#        self._conn.close()
#
#    def recv(self):
#        return self._conn.recv(1024)
#
#    def send(self, data):
#        self._conn.sendall(data)
