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

        self._rlist = [self]
        self._wlist = []
        self._xlist = []

    def fileno(self):
        return self._sock.fileno()

    def open(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self._sock.bind(self._addr)
        self._sock.listen(5)

        logging.info("Open server socket %s", self._sock)

    def close(self):
        self._sock.close()

        logging.info("Close server socket %s", self._sock)

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

    def find_client(self, sock=None, host=None, port=None):
        for r in self._rlist:
            if r.sock == sock or r.addr[0] == host or r.addr[1] == port:
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
        self._server.append_client(self)

        logging.info("Open server - client socket %s", self._sock)

    def close(self):
        self._server.remove_client(self)

        logging.info("Close server - client socket %s", self._sock)

    def recv(self): # TODO
        data = self._sock.recv(65535).decode("utf-8")
        return holepunch.message.Message(data)

    def send(self, message): # TODO
        self._sock.sendall(bytes(message))

    def handle(self):
        message = self.recv()
        print(message)

        if message.method == "<":
            client = self._server.find_client(host=message.body)

            if client:
                message = holepunch.message.Message(">{0}:{1}".format(self._addr[0], holepunch.config.HOLEPUNCH_PORT))
                client.send(message)
            else:
                message = holepunch.message.Message("?")
                self.send(message)

        elif message.method == "!":
            message = holepunch.message.Message("!")
            self.send(message)

        elif message.method == ".":
            self.close()

        logging.info("Handle server - client socket %s", self._sock)
