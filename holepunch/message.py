class Message:

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, value):
        self._method = value

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, value):
        self._body = value

    def __init__(self, data):
        self._method = None
        self._body = None

        self.parse(data)

    def __bytes__(self):
        pass

    def parse(self, data):
        if data:
            if data[0] in [">", "<", "!", "?"]:
                self._method = data[0]

                if data[0] == ">":
                    if data[1:] != "":
                        host, port = data[1:].split(":")
                        self._body = (host, int(port))
                else:
                    self._body = ""
            else:
                self._method = "?"
                self._body = ""
        else:
            self._method = "."
            self._body = ""
