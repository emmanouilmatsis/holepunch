import holepunch.server
import holepunch.client


def parse_args():
        argparse = __import__("argparse")

        parser = argparse.ArgumentParser(description="Holepunch")

        parser.add_argument(
                "application",
                type=str,
                choices=["server", "client"],
                help="application type"
                )

        parser.add_argument(
                "-d",
                "--destination",
                type=str,
                default=None,
                help="destination host"
                )

        args = parser.parse_args()

        return args


def main():
    args = parse_args()

    if args.application == "server":
        holepunch.server.Server().run()
    elif args.application == "client":
        holepunch.client.TCPClient().open(args.destination)


if __name__ == "__main__":
    main()
