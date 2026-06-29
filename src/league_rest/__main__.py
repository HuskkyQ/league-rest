import argparse


def main() -> int:
    parser = argparse.ArgumentParser(prog="league-rest")
    parser.add_argument("--smoke", action="store_true", help="run a smoke check")
    args = parser.parse_args()

    if args.smoke:
        print("league-rest smoke ok")
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
