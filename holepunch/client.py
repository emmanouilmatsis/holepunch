import logging
import select
import socket

import holepunch.config
import holepunch.message


class Client:

    def __init__(self):
        self._server_sock = None
        self._server_addr = (holepunch.config.SERVER_HOST, holepunch.config.SERVER_PORT)

    def open(self):
        logging.info("Open client%s", self._addr)

        self._server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self._server_sock.connect(self._server_addr)

    def close(self):
        logging.info("Close client%s", self._addr)

        self._server_sock.close()

    def connect(self, dest_addr):
        request = holepunch.message.Message(">{0}:{1}".format(dest_addr[0], dest_addr[1]))
        self._server_sock.sendall(message)

        response = self._server_sock.recv(65535)

        if response.method == ">":
            source_addr = ()
            dest_addr = response.body
            return self.holepunch(source_addr, dest_addr)
        else:
            return None

    def holepunch(self, source_addr, dest_addr):
        raise NotImplementedError


class UDPClient(Client):

    def __init__(self):
        super().__init__()

    def holepunch(self, source_addr, dest_addr):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

        sock.bind(source_arrd)

        sock.sendto(b">", dest_addr)

        return sock


class TCPClient(Client):

    def __init__(self):
        super().__init__()

    def holepunch(self, source_addr, dest_addr):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

        sock.bind(source_addr)

        while sock.connect_ex(dest_addr): pass

        return sock
