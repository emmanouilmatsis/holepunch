import logging
import select
import socket

import holepunch.config


class Server:

    def __init__(self):
        self._sock = None
        self._addr = (holepunch.config.HOST, holepunch.config.PORT)

        self._rlist = []
        self._wlist = []
        self._xlist = []

        self._clients = []

    def fileno(self):
        return self._sock

    def open(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self._sock.bind(self._addr)
        self._sock.listen(5)

        self._rlist.append(self._sock)

        logging.info("Open server%s.", self._addr)

    def close(self):
        self._sock.close()

        self._rlist.remove(self._sock)

        logging.info("Close server%s.", self._addr)

    def run(self):
        self.open()

        while True:
            try:
                rready, wready, xready = select.select(self._rlist, self._wlist, self._xlist)

                for socket in rready:
                    if socket == self._sock:
                        sock, addr = socket.accept()

                        client = Client(self, sock, addr)
                        client.open
                    else:
                        client = self.find_client(sock=socket)
                        client.handle()

            except KeyboardInterrupt:
                for client in self._clients:
                    client.close()
                break

        self.close()

    def find_client(self, sock=None, addr=None):
        for client in self._clients:
            if client.sock == sock or client.addr == addr:
                return client
        return None

    def append_client(self, client):
        self._clients.append(client)
        self._rlist.append(client.sock)

    def remove_client(self, client):
        self._clients.remove(client)
        self._rlist.remove(client.sock)


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

    def __init__(self, server, sock, addr):
        self._server = server
        self._sock = sock
        self._addr = addr

    def fileno(self):
        return self._sock

    def open(self):
        self._server.append_client(self)

        logging.info("Open client%s.", self._addr)

    def close(self):
        self._sock.close()
        self._server.remove_client(self)

        logging.info("Close client%s.", self._addr)

    def recv(self):
        data = self._sock.recv(holepunch.config.BUFSIZE)
        return data

    def send(self, data):
        self._sock.sendall(data)

    def handle(self):
        data = self.recv()

        if not data:
            self.close()

        logging.info("Handle client%s.", self._addr)


class Request:

    def __init__(self, data):
        self._data = data
        self._method = None
        self._body = None


class Response:

    def __init__(self, data):
        self._data = data
        self._method = None
        self._body = None
