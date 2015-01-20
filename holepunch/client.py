import logging
import select
import socket

import holepunch.config
import holepunch.message


class Server:

    def __init__(self):
        self._sock = None
        self._addr = (holepunch.config.SERVER_HOST, holepunch.config.SERVER_PORT)

    def _open(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self._sock.connect(self._addr)

        logging.info("Open client - server socket %s", self._sock)

    def _close(self):
        self._sock.close()

        logging.info("Close client - server socket %s", self._sock)

    def _send(self, message):
        data = bytes(message)
        self._sock.sendall(data)

    def _recv(self):
        data = self._sock.recv(65535)
        return holepunch.message.Message(data.decode("utf-8"))

    def listen_request(self):
        self._open()

        request = holepunch.message.Message(">")
        self._send(request)

        response = self._recv()

        self._close()

        return response

    def connect_request(self, dest_host):
        self._open()

        request = holepunch.message.Message("<{0}".format(dest_host))
        self._send(request)

        response = self._recv()

        self._close()

        return response


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

    def __init__(self):
        self._server = Server()
        self._sock = None
        self._addr = None

    def _holepunch(self, source_addr, dest_addr):
        raise NotImplementedError

    def fileno(self):
        return self._sock.fileno()

    def open(self, dest_host=None):
        """Open client - client socket.

        Open socket between source_host and dest_host on source_port and
        dest_port received by server.

        Args:
            dest_host: Destination host address. If dest_host is None then
            client will receive a connect request else will send a connect
            request.

        Raises:
            Exception: Excpetion if socket cannot open because response is not
            holepunch.
        """

        # Handle request
        if dest_host is None:
            response = self._server.listen_request()
        else:
            response = self._server.connect_request(dest_host)

        # Handle response
        if response.method == "*":
            source_addr = ("", response.body[1])
            dest_addr = response.body
            self._sock, self._addr = self.holepunch(source_addr, dest_addr)
        else:
            raise Exception(response)

        logging.info("Open client - client socket %s", self._sock)

    def close(self):
        """Close client - client socket.

        Close socket between source_host and dest_host on source_port and
        dest_port received by server.

        Raises:
            Exception: Excpetion if socket cannot close because socket is None.
        """

        self._sock.close()
        self._addr = None

        logging.info("Close client - client socket %s", self._sock)

    def send(self, data):
        """Send client - client data.

        Send data to connected client.

        Args:
            data: Data as bytes sent to client.
        """
        self._sock.sendall(data)

    def recv(self):
        """Receive client - client data.

        Receive data from connected client.

        Returns:
            data: Data as bytes received from client.
        """

        return self._sock.recv(65535)


class UDPClient(Client):

    def __init__(self):
        super().__init__()

    def _holepunch(self, source_addr, dest_addr):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

        sock.bind(source_arrd)

        sock.sendto(b"*", dest_addr)

        return (sock, dest_addr)


class TCPClient(Client):

    def __init__(self):
        super().__init__()

    def _holepunch(self, source_addr, dest_addr):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

        sock.bind(source_addr)

        while sock.connect_ex(dest_addr): pass

        return (sock, dest_addr)
