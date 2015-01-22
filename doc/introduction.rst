Introduction
============

Hole Punching
-------------
"Hole punching is a computer networking technique for establishing a direct
connection between two parties who are both behind restrictive firewalls. Each
client connects to an unrestricted third-party server that temporarily stores
external and internal address information from them. The server relays one
client's information to the other and vice versa, and both clients try to
establish a connection between each other. Having valid port numbers causes the
firewalls to accept the incoming packets from each side. Hole punching does not
require any knowledge of the network topology to function."

http://en.wikipedia.org/wiki/Hole_punching

Run Holepunch
-------------
Server has to run as a process on a machine with public ip address or port
forwarding. Clients can run by instantiating Client class on a machine behind a
NAT/Firewall.

Server::

    $ python -m holepunch server

Client 1::

    import holepunch.client

    client = holepunch.client.Client()
    client.open() # Send listen request and block wait to receive holepunch response

Client 2::

    import holepunch.client

    dest_host = "127.0.0.2" # Client1 host address
    client = holepunch.client.Client()
    client.open(dest_host) # Send connect request and block wait to receive holepunch response


Test Holepunch
--------------
To run Punchhole Server and Client on the same machine iptable rules need to be
added in order to simulate NAT/Firewall and each endpoint has to bind in
different host address.

IPTables
++++++++
To use Holepunch on a single machine you need to simulate a NAT/Firewall by a
chain of rules to the iptables.

IPTables setup::

    $ iptables -A INPUT -i lo --dport 20000 -j ACCEPT
    $ iptables -A INPUT -i lo -m state --state RELATED,ESTABLISHED -j ACCEPT
    $ iptables -A INPUT -i lo -j DROP

IPTables reset::

    $ iptables -F

A Server can use any loopback host address but must use the port address specified in the
holepunch.config file.

IP Addresses
++++++++++++
+-----------------+-----------------+-----------------+-----------------+
|                 |     Server      |    Client 1     |    Client 2     |
+-----------------+-----------------+-----------------+-----------------+
| Server - Client | 127.0.0.1:20000 |                 |                 |
+-----------------+-----------------+-----------------+-----------------+
| Client - Server |                 | 127.0.0.2:20000 | 127.0.0.3:20000 |
+-----------------+-----------------+-----------------+-----------------+
| Client - Client |                 | 127.0.0.2:20001 | 127.0.0.3:20001 |
+-----------------+-----------------+-----------------+-----------------+
