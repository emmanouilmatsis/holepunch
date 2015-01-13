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

        args = parser.parse_args()

        return args


def main():
    args = parse_args()

    if args.protocol == "tcp":
        server = holepunch.server.Server()
    elif args.protocol == "udp":
        server = holepunch.server.Server()

    server.run()


if __name__ == "__main__":
    main()
