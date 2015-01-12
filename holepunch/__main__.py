import holepunch.server


def parse_args():
        argparse = __import__("argparse")

        parser = argparse.ArgumentParser(description="Holepunch")

        parser.add_argument(
                "protocol",
                type=str,
                choices=["udp", "tcp"],
                help="protocol name"
                )

        parser.add_argument(
                "port",
                type=int,
                help="port name"
                )

        args = parser.parse_args()

        return args


def main():
    args = parse_args()

    if args.protocol == "tcp":
        #server = holepunch.server.TCPServer(args.port)
        server = holepunch.server.Server(args.port)
    elif args.protocol == "udp":
        server = holepunch.server.UDPServer(args.port)

    server.run()


if __name__ == "__main__":
    main()
