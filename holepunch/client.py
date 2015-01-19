import logging
import select
import socket

import holepunch.config
import holepunch.message


class Server:

    @property
    def sock(self):
        return self._sock

    @sock.setter
    def sock(self, value):
        self._sock = value

    @property
    def addr(self):
        return self._addr

    @addr.setter
    def addr(self, value):
        self._addr = value

    def __init__(self):
        self._sock = None
        self._addr = (holepunch.config.SERVER_HOST, holepunch.config.SERVER_PORT)

    def open(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self._sock.connect(self._addr)

        logging.info("Open client - server socket %s", self._sock)

    def close(self):
        self._sock.close()

        logging.info("Open client - server socket %s", self._sock)

    def recv(self):
        data = self._sock.recv(65535)
        return holepunch.message.Message(data)

    def send(self, message):
        self._sock.sendall(message)


class Client:

    @property
    def sock(self):
        return self._sock

    @sock.setter
    def sock(self, value):
        self._sock = value

    @property
    def addr(self):
        return self._addr

    @addr.setter
    def addr(self, value):
        self._addr = value

    def __init__(self):
        self._server = Server()
        self._sock = None
        self._addr = None

    def open(self, dest_host):
        self._server.open()

        message = holepunch.message.Message("<{0}".format(dest_host))
        self._server.send(message)

        message = self._server.recv()
        if message.method == ">":
            source_addr = ("", message.body[1])
            dest_addr = message.body
            self._sock, self._addr = self.holepunch(source_addr, dest_addr)
        else:
            raise Exception(message)

        logging.info("Open client - client socket %s", self._sock)

    def close(self):
        self._server.close()

        self._sock.close()
        self._addr = None

        logging.info("Close client - client socket %s", self._sock)

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

        return (sock, dest_addr)


class TCPClient(Client):

    def __init__(self):
        super().__init__()

    def holepunch(self, source_addr, dest_addr):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

        sock.bind(source_addr)

        while sock.connect_ex(dest_addr): pass

        return (sock, dest_addr)
