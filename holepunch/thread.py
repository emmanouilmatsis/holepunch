import threading
import socket
import queue

import holepunch.config


class Server:

    def __init__(self):
        self._conn = None
        self._addr = (holepunch.config.HOST, holepunch.config.PORT)

        self._lock = threading.Lock()
        self._tasks = queue.Queue()
        self._workers = [Worker(self, self._tasks) for _ in range(holepunch.config.WORKERS_SIZE)]

    def _open(self):
        print("opening...")
        self._conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self._conn.bind(self._addr)
        self._conn.listen(5)

        for worker in self._workers:
            worker.start()

    def _close(self):
        print("closing...")
        self._conn.shutdown(socket.SHUT_RDWR)
        self._conn.close()

        for worker in self._workers:
            worker.stop()

    def run(self):
        self._open()

        while True:
            try:
                conn, addr = self._conn.accept()
                task = holepunch.Task(conn, addr)
                self._tasks.put(task)
            except KeyboardInterrupt:
                break

        self._close()


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
            task.execute()


class Task:

    def __init__(self, conn, addr):
        super().__init__()

        self._conn = conn
        self._addr = addr

    def execute(self):
        data = self._conn.recv(holepunch.config.BUFSIZE)
        self._conn.sendall(data.encode("utf-8"))
        self._conn.shutdown(socket.SHUT_RDWR)
        self._conn.close()
