import argparse
from core.scanner import WebScanner


def main():

    parser = argparse.ArgumentParser(
        description="Mini Web Vulnerability Scanner"
    )

    parser.add_argument(
        "--url",
        required=True,
        help="Target URL"
    )

    parser.add_argument(
        "--depth",
        type=int,
        default=2,
        help="Crawler depth"
    )

    args = parser.parse_args()

    target_url = args.url
    depth = args.depth

    print("================================")
    print(" Mini Web Vulnerability Scanner ")
    print("================================")

    scanner = WebScanner(target_url, depth)

    scanner.start()


if __name__ == "__main__":
    main()