import socket


def server():
    self._conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self._conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self._conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    self._conn.bind(("", sys.argv[2]))
    self._conn.listen(5)

    conn, addr = self._conn.accept()
    print("<{0}:{1}> <- <{2}:{3}>".format(host, port, conn[0], conn[1])

    self._conn.close()


def client():
    self._conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self._conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self._conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    self._conn.bind(("", sys.argv[2]))

    conn, addr = self._conn.connect()
    print("<{0}:{1}> -> <{2}:{3}>".format(host, port, conn[0], conn[1])

    self._conn.close()


if __name__ == "__main__":

    if sys.argv[1] == "server":
        server(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "client":
        client(sys.argv[2], sys.argv[3])
