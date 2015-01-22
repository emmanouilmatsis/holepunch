"""Client for P2P communication across NAT/Firewall.

Instantiation of Client class will unable P2P communication across NAT/Firewall
between source and destination by sending a listen or connect request to a
holepunch server. Holepunch server response will be either an error or holepunch
which will call holepunch method on client and return a client-client P2P
socket.

Example:
    Listening client::

        client1_host = xxx.xxx.xxx.xxx
        client1 = holepunch.Client()
        client1.open() # Block waiting for holepunch response
        client1.send("OK")

    Connecting client::

        client2 = helepunch.Client()
        client2.open(client1_host) # Block waiting for holepunch response
        data = client2.recv()
        print(data.decode("utf-8"))
"""


import logging
import socket

import holepunch.config
import holepunch.message


class Client:
    """Socket wrapper for P2P communication across NAT/Firewall.

    Socket wrapper for P2P communication across NAT/Firewall opened by
    requesting the holepunching server to introduce source to dest. On holepunch
    (*) server response each client will send UDP/TCP packet with source address
    and destination address.

    Attributes:
        _server: Holepunch server socket wrapper.
        _sock:  Client-client socket.
        _addr:  Client host and port address tuple.
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
        """Initialise client."""

        self._server = Server()
        self._sock = None
        self._addr = None

    def _holepunch(self, source_addr, dest_addr):
        """Punch hole on NAT/Firewall.

        Punch hole on Nat/Firewall and open a socket by sending TCP or UDP
        packets from source address to destination address.

        Args:
            source_addr: Tuple of source host address and source port address.
            dest_addr: Tuple of dest host address and dest port address.

        Returns:
            sock: Client-client (p2p) socket between endpoints behind
            NAT/Firewall.
            addr: Tuple of dest host address and dest port address.
        """

        raise NotImplementedError

    def fileno(self):
        """Get client-client socket file descriptor.

        Get client-client socket file descriptor to unable use of self with
        select.

        Returns:
            file_descriptor: Client-client socket file descriptor.
        """

        return self._sock.fileno()

    def open(self, dest_host=None):
        """Open client-client socket.

        Open socket between source_host and dest_host on source_port and
        dest_port received by server.

        Args:
            dest_host: Destination host address. If dest_host is None then client will receive a connect request else will send a connect request.

        Raises:
            Exception: Excpetion if socket cannot open because response is not holepunch.
        """

        # Handle request
        if dest_host is None:
            # Listen (<) request
            response = self._server.listen_request()
        else:
            # Connect (>dest_host) request
            response = self._server.connect_request(dest_host)

        # Handle response
        if response.method == "*":
            # Holepunch (*(dest_host, dest_port)) response
            source_addr = ("", response.body[1])
            dest_addr = response.body
            self._sock, self._addr = self._holepunch(source_addr, dest_addr)
        else:
            # NotFound (?), Close (.) response
            raise Exception(response)

        logging.info("Open client-client socket %s", self._sock)

    def close(self):
        """Close client-client socket.

        Close socket between source_host and dest_host on source_port and
        dest_port received by server.

        Raises:
            Exception: Excpetion if socket cannot close because socket is None.
        """

        self._sock.close()
        self._addr = None

        logging.info("Close client-client socket %s", self._sock)

    def send(self, data):
        """Send client-client data.

        Send data to client.

        Args:
            data: Data as bytes sent to client.
        """

        self._sock.sendall(data)

    def recv(self):
        """Receive client-client data.

        Receive maximum data from client.

        Returns:
            data: Data as bytes received from client.
        """

        return self._sock.recv(65535)


class UDPClient(Client):
    """Socket wrapper for UDP P2P communication across NAT/Firewall.

    Socket wrapper for UDP P2P communication across NAT/Firewall opened by
    requesting the holepunching server to introduce source to dest. On holepunch
    (*) server response each client will send UDP packet with source address
    and destination address.

    Attributes:
        _server: Holepunch server socket wrapper.
        _sock:  Client-client socket.
        _addr:  Client host address and port address tuple.
    """

    def __init__(self):
        """ Initialise UDPClient."""

        super().__init__()

    def _holepunch(self, source_addr, dest_addr):
        """Punch hole on NAT/Firewall with UDP packet.

        Punch hole on Nat/Firewall and open a socket by sending a UDP (*)
        packet from source address to destination address.

        Args:
            source_addr: Tuple of source host address and source port address.
            dest_addr: Tuple of dest host address and dest port address.

        Returns:
            sock: Client-client (p2p) socket between endpoints behind
            NAT/Firewall.
            addr: Tuple of dest host address and dest port address.
        """

        # Open UDP socket for P2P communication
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

        # Bind socket to source_addr received by holepunch server
        sock.bind(source_addr)

        # Send UDP holepunch packet (non-blocking)
        sock.sendto(b"*", dest_addr)

        # Return socket, dest_addr tuple
        return (sock, dest_addr)


class TCPClient(Client):
    """Socket wrapper for TCP P2P communication across NAT/Firewall.

    Socket wrapper for TCP P2P communication across NAT/Firewall opened by
    requesting the holepunching server to introduce source to dest. On holepunch
    (*) server response each client will send TCP packet with source address
    and destination address.

    Attributes:
        _server: Holepunch server socket wrapper.
        _sock:  Client-client socket.
        _addr:  Client host address and port address tuple.
    """

    def __init__(self):
        """Intialise TCPClient."""

        super().__init__()

    def _holepunch(self, source_addr, dest_addr):
        """Punch hole on NAT/Firewall with TCP packet.

        Punch hole on Nat/Firewall and open a socket by sending a TCP (SYN)
        packet from source address to destination address.

        Args:
            source_addr: Tuple of source host address and source port address.
            dest_addr: Tuple of dest host address and dest port address.

        Returns:
            sock: Client-client (p2p) socket between endpoints behind
            NAT/Firewall.
            addr: Tuple of dest host address and dest port address.
        """

        # Open TCP socket for P2P communication
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

        # Bind socket to source_addr received by holepunch server
        sock.bind(source_addr)

        # Send TCP holepunch packet (blocking)
        while sock.connect_ex(dest_addr):
            pass

        # Return socket, dest_addr tuple
        return (sock, dest_addr)


class Server:
    """Holepunch server socket wrapper for client-client P2P communication.

    Holepunch server socket wrapper for client-client P2P communication
    handling of request. Response will be either an error (NotFound (?), Close
    (.)) or holepunch (Holepunch (*)).

    Attributes:
        _sock:  Server - client socket.
        _addr: Server host address and port address tuple.
    """

    def __init__(self):
        """Initialise server."""

        self._sock = None
        self._addr = (holepunch.config.SERVER_HOST, holepunch.config.SERVER_PORT)

    def open(self):
        """Open client-server socket.

        Open socket between source_host on source_port and server dest_host on
        dest_port as configured in the config file.
        """

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

        self._sock.connect(self._addr)


        logging.info("Open client-server socket %s", self._sock)

    def close(self):
        """Close client-server socket.

        Close socket between source_host on source_port and server dest_host on
        dest_port as configured in the config file.
        """

        self._sock.close()

        logging.info("Close client-server socket %s", self._sock)

    def send(self, message):
        """Send client-client data.

        Send message to server.

        Args:
            message: Parsed data received from client.
        """

        data = bytes(message)
        self._sock.sendall(data)

    def recv(self):
        """Receive client-client data.

        Receive maximum data from sever.

        Returns:
            message: Parsed data received from client.
        """

        data = self._sock.recv(65535)
        return holepunch.message.Message(data.decode("utf-8"))

    def listen_request(self):
        """Send listen request to server.

        Send listen request (<) to server and the block wait for response.

        Returns:
            response: Server response.
        """

        self.open()

        # Send listen request to holepunch server
        request = holepunch.message.Message("<")
        self.send(request)

        # Receive holepunch or error response (blocking)
        response = self.recv()

        self.close()

        return response

    def connect_request(self, dest_host):
        """Send connect request to server.

        Send connect request (>dest_host) to server and the block wait for
        response.

        Args:
            dest_host: Destination host address.

        Returns:
            response: Server response.
        """

        self.open()

        # Send connect request to holepunch server
        request = holepunch.message.Message(">{0}".format(dest_host))
        self.send(request)

        # Receive holepunch or error response (blocking)
        response = self.recv()

        self.close()

        return response
