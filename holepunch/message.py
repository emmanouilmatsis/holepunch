"""Message encapsulating request/response between client - server

Classes client.Server and server.client depend on Message for request/response
exchange. There are 3 request and 3 responses.

Messages:

    +---------------------------+-------------------+--------------------------------------+
    | Message                   | Type              | Description                          |
    +===========================+===================+======================================+
    | >dest_host                | request           | connect to dest_host                 |
    +---------------------------+-------------------+--------------------------------------+
    | <                         | request           | listen                               |
    +---------------------------+-------------------+--------------------------------------+
    | \*(dest_host, dest_port)  | response          | holepunch to (dest_host, dest_port)  |
    +---------------------------+-------------------+--------------------------------------+
    | !                         | response          | not found                            |
    +---------------------------+-------------------+--------------------------------------+
    | .                         | request/response  | close socket                         |
    +---------------------------+-------------------+--------------------------------------+
"""


class Message:
    """Request/Response message for client - server communication.

    Encapsulate parsed string to message format with method and body.

    Attributes:
        _method: Request/Response method.
        _body: Request/Response body.
    """

    @property
    def method(self):
        """Method accessor."""
        return self._method

    @method.setter
    def method(self, value):
        """Method mutator."""
        self._method = value

    @property
    def body(self):
        """Body accessor."""
        return self._body

    @body.setter
    def body(self, value):
        """Body mutator."""
        self._body = value

    def __init__(self, data):
        """Message intialisation."""
        self._method = None
        self._body = None

        self.parse(data)

    def __repr__(self):
        """__repr__ overload."""
        return "Message({0}{1})".format(self._method, self._body)

    def __str__(self):
        """__str__ overload."""
        return "{0}{1}".format(self._method, self._body)

    def __bytes__(self):
        """__bytes__ overload."""
        return bytes("{0}{1}".format(self._method, self._body), "utf-8")

    def __format__(self, format_spec=""):
        """__format___ overload."""
        return "{0}{1}".format(self._method, self._body)

    def parse(self, data):
        """Parse String data.

        Parse String data to method and body request/response format.

        Args:
            data: String data to be parsed.
        """
        if data:
            if data[0] == ">": # >dest_host
                self._method = data[0]
                self._body = data[1:]
            elif data[0] == "<": # <
                self._method = data[0]
                self._body = ""
            elif data[0] == "*": # *dest_host, dest_port)
                self._method = data[0]
                self._body = eval(data[1:])
            elif data[0] == "?": # ?
                self._method = data[0]
                self._body = ""
        else: # .
            self._method = "."
            self._body = ""
