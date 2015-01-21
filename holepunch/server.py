"""Holepunch server for P2P communication across NAT/Firewall.

Holepunch server process is listening for clients. A client can send a connect
or listen request and receive a holepunch or error response. Holepunch server
will send a holepunch response to the connect and listen client with the
destination host address and destination port address. Holepunch server will
bind on the address snd will set a holepunch response to the port set in config
file.
"""


import logging
import select
import socket

import holepunch.config
import holepunch.message


class Server:
    """Holepunch server for P2P communication across NAT/Firewall.

    Holepunch server is listening for client and will introduce clients from its
    client list. It is using select to for asynchronous i/o, accepting new
    clinets when server is ready and handling request/response when client is
    ready.

    Attributes:
        _sock:  Server-client socket.
        _addr:  Server host address and port address tuple.
        _rlist: Read ready file descriptors
        _wlist: Write ready file descriptors
        _xlist: Exception ready file descriptors
    """

    @property
    def sock(self):
        """Sock accessor."""
        return self._sock

    @sock.setter
    def sock(self, value):
        """Sock mutator."""
        self._sock = value

    @property
    def addr(self):
        """Addr accessor."""
        return self._addr

    @addr.setter
    def addr(self, value):
        """Addr mutator."""
        self._addr = value

    def __init__(self):
        """Initialise server."""

        self._sock = None
        self._addr = (holepunch.config.SERVER_HOST, holepunch.config.SERVER_PORT)

        self._rlist = [self]
        self._wlist = []
        self._xlist = []

    def fileno(self):
        """Get server socket file descriptor.

        Get server socket file descriptor to unable use of self with
        select.

        Returns:
            file_descriptor: Server socket file descriptor.
        """

        return self._sock.fileno()

    def open(self):
        """Open listening socket.

        Open socket, bind on host and port as configured in the config file and
        start listening for clients.
        """

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self._sock.bind(self._addr)
        self._sock.listen(5)

        logging.info("Open server socket %s", self._sock)

    def close(self):
        """Close listening socket.

        Close socket, and consiquently all server-client sockets.
        """

        self._sock.close()

        logging.info("Close server socket %s", self._sock)

    def accept_client(self):
        """Accept server-client connection.

        Accept server-client connections, instantiate and open client.
        Client will append it self on the server ready list.
        """

        sock, addr = self._sock.accept()
        client = Client(self)
        client.open(sock, addr)

    def find_client(self, sock=None, host=None, port=None):
        """Find client from ready list.

        Find client in client list by socket file descriptor or host address or
        port address.

        Args:
            sock: Client socket file descriptor.
            host: Client host address.
            port: Client port address.
        """

        for r in self._rlist:
            if r.sock == sock or r.addr[0] == host or r.addr[1] == port:
                return r
        return None

    def append_client(self, client):
        """Append client to ready list.

        Append client to ready list. Ready list is used by select for selecting
        server or clients which their socket file descriptors are ready to read.

        Args:
            client: Client to append in ready list.
        """

        self._rlist.append(client)

    def remove_client(self, client):
        """Remove client from ready list.

        Remove client from ready list. Ready list is used by select for
        selecting server or clients which their socket file descriptors are
        ready to read.

        Args:
            client: Client to remove in ready list.
        """

        self._rlist.remove(client)

    def run(self):
        """Run holepunch server.

        Run continues loop for accept or handle clients.
        Break loop when KeyboardInterrupt.
        """

        self.open()

        while True:
            try:
                # Asynchronous I/O
                rready, wready, xready = select.select(self._rlist, self._wlist, self._xlist)

                for r in rready:
                    if r is self: # Handle server
                        r.accept_client()
                    else: # Handle client
                        r.handle()

            except KeyboardInterrupt:
                break

        self.close()


class Client:
    """Server-client socket wrapper.

    Server-client socket wrapper used by select asynchronous i/o for handling
    request/repsonse. Its client represents a server-client endpoint.

    Attributes:
        _server: Holepunch server socket wrapper.
        _sock:  Client - client socket.
        _addr:  Client host address and port address tuple.
    """

    @property
    def sock(self):
        """Sock accessor."""
        return self._sock

    @sock.setter
    def sock(self, value):
        """Sock mutator."""
        self._sock = value

    @property
    def addr(self):
        """Addr accessor."""
        return self._addr

    @addr.setter
    def addr(self, value):
        """Addr mutator."""
        self._addr = value

    def __init__(self, server):
        """Initialise server."""

        self._server = server
        self._sock = None
        self._addr = None

    def fileno(self):
        """Get server-client socket file descriptor.

        Get server-client socket file descriptor to unable use of self with
        select.

        Returns:
            file_descriptor: Server-client socket file descriptor.
        """

        return self._sock.fileno()

    def open(self, sock, addr):
        """Open server-client socket.

        Append self from server ready list.
        """

        # Open socket
        self._sock = sock
        self._addr = addr

        # Append to server client list
        self._server.append_client(self)

        logging.info("Open server-client socket %s", self._sock)

    def close(self):
        """Close server-client socket.

        Close socket and remove self from server ready list.
        """

        # Close socket
        self._sock.close()
        self._addr = None

        # Remove from server client list
        self._server.remove_client(self)

        logging.info("Close server-client socket %s", self._sock)

    def send(self, message):
        """Send server-client data.

        Send message to server.

        Args:
            message: Parsed data received from client.
        """

        data = bytes(message)
        self._sock.sendall(data)

    def recv(self):
        """Receive server-client data.

        Receive maximum data from sever.

        Returns:
            message: Parsed data received from client.
        """

        data = self._sock.recv(65535)
        return holepunch.message.Message(data.decode("utf-8"))

    def handle(self):
        """Handle server-client socket file descriptor

        Handle server-client socket file descriptor when is read ready. After
        receive request, depending on the request method the appropriate respond
        will be send to client.
        """

        logging.info("Handle server-client socket %s", self._sock)

        # Receive request
        request = self.recv()

        if request.method == ">": # Handle connect request
            # Find listening client in server client list
            client = self._server.find_client(host=request.body)

            if client:
                # Send holepunch response to connect client
                response = holepunch.message.Message("*{0}".format((client.addr[0], holepunch.config.HOLEPUNCH_PORT)))
                self.send(response)

                # Send holepunch response to listen client
                response = holepunch.message.Message("*{0}".format((self.addr[0], holepunch.config.HOLEPUNCH_PORT)))
                client.send(response)
            else:
                # Send client not found response
                response = holepunch.message.Message("?")
                self.send(response)

        elif request.method == "<": # Handle listen request
            # Client is listening for holepunch response
            pass

        elif request.method == ".": # Handle close request
            # Close client
            self.close()
