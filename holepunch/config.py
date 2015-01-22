import logging


logging.basicConfig(
    filename=None,
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.DEBUG
)

# Holepunch server host and port
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 20000

# Holepunch port for P2P communication behind NAT/Firewall
HOLEPUNCH_PORT = 20001
