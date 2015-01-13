import logging


logging.basicConfig(
    filename=None,
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.DEBUG
)

HOST = ""
PORT = 1234
BACKLOG = 5
BUFSIZE = 1024

WORKERS_SIZE = 32
