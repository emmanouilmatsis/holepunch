import socket


class Server:

    def __init__(self, port):
        self._port = port

    def introduce(self, session=None):
        pass

    def run(self):
        raise NotImplementedError


class UDPServer:

    def __init__(self, port):
        super().__init__(port)

    def run(self):
        pass


class TCPServer:

    def __init__(self, port):
        super().__init__(port)

    def run(self):
        pass
