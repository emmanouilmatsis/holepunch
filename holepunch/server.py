import logging
import select
import socket

import holepunch.config


class Server:

    def __init__(self):
        self._sock = None
        self._addr = (holepunch.config.HOST, holepunch.config.PORT)

        self._rlist = [self]
        self._wlist = []
        self._xlist = []

    def fileno(self):
        return self._sock.fileno()

    def open(self):
        logging.info("Open server%s", self._addr)

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self._sock.bind(self._addr)
        self._sock.listen(5)

    def close(self):
        logging.info("Close server%s", self._addr)

        self._sock.close()

    def run(self):
        self.open()

        while True:
            try:
                rready, wready, xready = select.select(self._rlist, self._wlist, self._xlist)

                for r in rready:
                    if r is self:
                        r.accept_client()
                    else:
                        r.handle()

            except KeyboardInterrupt:
                break

        self.close()

    def accept_client(self):
        sock, addr = self._sock.accept()
        client = Client(self, sock, addr)
        client.open()

    def find_client(self, sock=None, addr=None):
        for r in self._self._rlist:
            if r.sock == sock or r.addr == addr:
                return r
        return None

    def append_client(self, client):
        self._rlist.append(client)

    def remove_client(self, client):
        self._rlist.remove(client)


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
        return self._sock.fileno()

    def open(self):
        logging.info("Open client%s", self._addr)

        self._server.append_client(self)

    def close(self):
        logging.info("Close client%s", self._addr)

        self._server.remove_client(self)

    def recv(self):
        data = self._sock.recv(holepunch.config.BUFSIZE)
        return Message(data)

    def send(self, message):
        self._sock.sendall(message)

    def handle(self):
        logging.info("Handle client%s", self._addr)

        data = self.recv()

        if not data:
            self.close()


class Message:

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, value):
        self._method = value

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, value):
        self._body = value

    def __init__(self, data):
        self._method = None
        self._body = None

        self.parse(data)

    def __bytes__(self):
        pass

    def validate(self, data):
        isMethod = data[0] in [">", "<", "!", "?"]
        isBody

    def parse(self, data):
        method = data[0]
        body = data[1:]

        if method in [">", "<", "!", "?"]:
            if method == ">":
