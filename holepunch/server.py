import socket
import queue

import holepunch.session
import holepunch.config


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
            dready, wready, xready = select.select(rlist, wlist, xlist)


class Client:

    def __init__(self, conn, addr):
        self._conn = conn
        self._addr = addr

    def 
    http://ilab.cs.byu.edu/python/threadingmodule.html
    http://ilab.cs.byu.edu/python/select/echoserver.html
    https://pythonadventures.wordpress.com/2013/07/06/a-basic-socket-client-server-example/
