import logging
import select
import socket

import holepunch.config


class Server:

    def __init__(self):
        self._conn = None
        self._addr = (holepunch.config.HOST, holepunch.config.PORT)

        self._rlist = []
        self._wlist = []
        self._xlist = []

        self._clients = []

    def open(self):
        self._conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self._conn.bind(self._addr)
        self._conn.listen(5)

        self._rlist.append(self._conn)

        logging.info("Server%s is open.", self._addr)

    def close(self):
        self._conn.close()

        self._rlist.remove(self._conn)

        logging.info("Server%s is closed.", self._addr)

    def run(self):
        self.open()

        while True:
            try:
                rready, wready, xready = select.select(self._rlist, self._wlist, self._xlist)
                for socket in rready:
                    handler = self if self._conn == socket else self.find_client(conn=socket)
                    handler.handle()
            except KeyboardInterrupt:
                break

        self.close()

    def handle(self):
        conn, addr = self._conn.accept()
        self.append_client(Client(self, conn, addr))

        logging.info("Server%s is connected to Client%s.", self._addr, addr)

    def find_client(self, conn=None, addr=None):
        for client in self._clients:
            if client._conn == conn or client._addr == addr:
                return client
        return None

    def append_client(self, client):
        self._clients.append(client)
        self._rlist.append(client._conn)

    def remove_client(self, client):
        self._clients.remove(client)
        self._rlist.remove(client._conn)


http://basyl.co.uk/code/punch/doc/files/Readme-txt.html

class Client:

    def __init__(self, server, conn, addr):
        self._server = server
        self._conn = conn
        self._addr = addr

    def recv(self):
        data = self._conn.recv(holepunch.config.BUFSIZE)
        return Request(data)

    def send(self, response):
        self._conn.sendall(response.encode("utf-8"))

    def handle(self):
        request = self.recv()

        if request.method == "INTRODUCE":
            client = self._server.find_client(addr=request.data)
            if client is not None:
                self.send(Response("HOLEPUNCH", client._addr))
                client.send(Response("HOLEPUNCH", self._addr))

        elif request.method == "CLOSE":
            self._conn.close()
            self._server.remove_client(self)

        else:
            self.send(Response("BAD REQUEST"))

        logging.info("Server%s is handling request from Client%s.", self._server._addr, self._addr)


class Request:

    def __init__(self, data):
        self._data = data


class Response:

    def __init__(self, code=None, method=None, data=None):
        pass
