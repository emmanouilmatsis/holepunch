import holepunch.server
import holepunch.client


def parse_args():
        argparse = __import__("argparse")

        parser = argparse.ArgumentParser(description="Holepunch")

        parser.add_argument("application",
                type=str,
                choices=["server", "client"],
                help="application type"
                )

        parser.add_argument("protocol",
                nargs="?",
                default=None,
                type=str,
                choices=["udp", "tcp"],
                help="destination host"
                )

        parser.add_argument("destination",
                nargs="?",
                default=None,
                type=str,
                help="destination host"
                )

        args = parser.parse_args()

        if args.application == "client" and args.protocol is None:
                parser.error("the following arguments are required: protocol, destination")

        return args


def main():
    args = parse_args()

    if args.application == "server":
        holepunch.server.Server().run()
    elif args.application == "client":
        if args.protocol == "udp":
            holepunch.client.TCPClient().open(args.destination)
        elif args.protocol == "tcp":
            holepunch.client.TCPClient().open(args.destination)


if __name__ == "__main__":
    main()
