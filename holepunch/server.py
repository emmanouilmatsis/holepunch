import socket
import queue

import holepunch.session


class Server:

    def __init__(self, port):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self._socket.bind(("", port))
        self._socket.listen(5)

        self._clients = []

    def run(self):
        while True:
            conn, addr = self._socket.accept()

            client = holepunch.client.Client(conn, addr)
            client.start()

            self._clients.append(client)


class Client(threading.Thread):

    def __init__(self, conn, addr):
        self._conn = conn
        self._addr = addr

    def run(self):
        while True:
            data = self._conn.recv(1024)
            if not data:
                break

            self._handle(data)

        self._conn.close()
