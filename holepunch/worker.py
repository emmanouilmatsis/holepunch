import sockets
import threading

import holepunch.request


class Worker(threading.Thread):

    def __init__(self, lock, tasks):
        threading.Thread.__init__(self)
        self._tasks = tasks

    def start(self):
        threading.Thread.start(self)
        self._running = True

    def stop(self):
        self._running = False

    def run(self):
        while self._running:
            task = self._tasks.get()
            while not task.done:
                task.execute()
            break


class Task:

    @property
    def done(self):
        return self._done

    @done.setter
    def done(self, value):
        self._done = value

    def __init__(self, lock):
        self._lock = lock
        self._done = False

    def execute(self):
        raise NotImplementedError


class ClientTask(holepunch.Task):

    def __init__(self, lock, client):
        super().__init__(lock)
        self._client = client

    def _parse(self, data):
        return self.holepunch.request.Request(data)

    def _handle(self, data):
        request = self._parse(data)

    def execute(self):
        data = self._client.recv()
        if not data:
            self._client.close()
            self._complete = True

        request = self._parse(data)
        self._handle(request)


class Client:

    def __init__(self, server, conn, addr):
        self._server = server
        self._conn = conn
        self._addr = addr

    def open(self):
        pass

    def close(self):
        self._conn.shutdown(socket.SHUT_RDWR)
        self._conn.close()

    def recv(self):
        return self._conn.recv(1024)

    def send(self, data):
        self._conn.sendall(data)
