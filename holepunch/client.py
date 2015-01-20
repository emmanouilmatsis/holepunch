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

    def send(self, message):
        data = bytes(message)
        self._sock.sendall(data)

    def recv(self):
        data = self._sock.recv(65535)
        return holepunch.message.Message(data.decode("utf-8"))

    def send_request(self, dest_host):
        message = holepunch.message.Message("<{0}".format(dest_host))
        self.send(message)

    def recv_request(self):
        message = self.recv()

        if message.method == ">":
            source_addr = ("", message.body[1])
            dest_addr = message.body
            return source_addr, dest_addr
        else:
            raise Exception(message)

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

    def open(self, dest_host=None):
        self._server.open()

        if dest_host is not None:
            self._server.send_request(dest_host)

        source_addr, dest_addr = self._server.recv_request()

        self._sock, self._addr = self.holepunch(source_addr, dest_addr)

        self._server.send_request(dest_addr)

        self._server.close()

        logging.info("Open client - client socket %s", self._sock)

    def close(self):
        self._sock.close()
        self._addr = None

        logging.info("Close client - client socket %s", self._sock)

    def send(self, data):
        self._sock.sendall(data)

    def recv(self):
        return self._sock.recv(65535)

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
        logging.info("Holepunch client - client socket %s", self._sock)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

        sock.bind(source_addr)

        while sock.connect_ex(dest_addr): pass

        return (sock, dest_addr)
