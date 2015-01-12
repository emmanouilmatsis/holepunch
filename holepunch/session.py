import threading
import socket


class Session(threading.Thread):

    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        self._conn = conn
        self._addr = addr

    def _handle(self, data):
        try:
            addr = self._parse(data)
        except:
            pass
        else:
            print(addr)

    def _close(self):
        self._conn.shutdown(socket.SHUT_RDWR)
        self._conn.close()

    def _parse(self, data):
        host, port = data.decode("utf-8").split(":")
        addr = (host, int(port))
        return addr

    def run(self):
        while True:
            data = self._conn.recv(1024)
            if not data:
                break

            self._handle(data)

        self._close()
