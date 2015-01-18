import logging
import select
import socket

import holepunch.config
import holepunch.message


class Server:

    def __init__(self):
        self._sock = None
        self._addr = (holepunch.config.SERVER_HOST, holepunch.config.SERVER_PORT)

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
        data = self._sock.recv(65535)
        return holepunch.message.Message(data)

    def send(self, message):
        self._sock.sendall(message)

    def handle(self):
        logging.info("Handle client%s", self._addr)

        message = self.recv()

        if message.method = ">":
            client = self._server.find_client(message.body)

            if client:
                message.body = "{0}:{1}".format(self._addr[0], self_addr[1])
                client.send(message)
            else:
                message.body = "!"
                self.send(message)

        elif message.method = "?":
            self.send(message)

        elif message.method = ".":
            self.close()
