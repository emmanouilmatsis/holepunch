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

    def __repr__(self):
        return "Message({0}{1})".format(self._method, self._body)

    def __str__(self):
        return "{0}{1}".format(self._method, self._body)

    def __bytes__(self):
        return bytes("{0}{1}".format(self._method, self._body), "utf-8")

    def __format__(self, format_spec=""):
        return "{0}{1}".format(self._method, self._body)

    def parse(self, data):
        if data:
            if data[0] in ["<", ">", "!", "?"]:
                self._method = data[0]

                if data[0] == "<":
                    self._body = data[1:]
                elif data[0] == ">":
                    self._body = eval(data[1:])
                else:
                    self._body = ""
            else:
                self._method = "?"
                self._body = ""
        else:
            self._method = "."
            self._body = ""
