import argparse
import sys

from .window_focus import (
    BrowserTarget,
    UnsupportedPlatformError,
    WindowTarget,
    WindowsWindowController,
    focus_browser,
    focus_game,
)


def main() -> int:
    parser = argparse.ArgumentParser(prog="league-rest")
    parser.add_argument("--smoke", action="store_true", help="run a smoke check")
    subparsers = parser.add_subparsers(dest="command")

    windows_parser = subparsers.add_parser("windows", help="list visible Windows desktop windows")
    windows_parser.set_defaults(command="windows")

    browser_parser = subparsers.add_parser("open-browser", help="open or focus a browser URL")
    browser_parser.add_argument("--url", required=True)
    browser_parser.add_argument("--window-hint")
    browser_parser.set_defaults(command="open-browser")

    game_parser = subparsers.add_parser("focus-game", help="focus a game window")
    game_parser.add_argument("--title")
    game_parser.add_argument("--process")
    game_parser.set_defaults(command="focus-game")

    args = parser.parse_args()

    if args.smoke:
        print("league-rest smoke ok")
        return 0

    try:
        if args.command == "windows":
            controller = WindowsWindowController()
            for window in controller.list_windows():
                print(f"{window.handle}\t{window.pid}\t{window.process_name}\t{window.title}")
            return 0

        if args.command == "open-browser":
            controller = WindowsWindowController()
            focused = focus_browser(BrowserTarget(args.url, args.window_hint), controller)
            if focused is None:
                print(f"opened browser url: {args.url}")
            else:
                print(f"focused browser window: {focused.title}")
            return 0

        if args.command == "focus-game":
            if not args.title and not args.process:
                parser.error("focus-game requires --title or --process")
            controller = WindowsWindowController()
            focused = focus_game(WindowTarget(args.title, args.process), controller)
            print(f"focused game window: {focused.title}")
            return 0
    except UnsupportedPlatformError as error:
        print(str(error), file=sys.stderr)
        return 2
    except LookupError as error:
        print(str(error), file=sys.stderr)
        return 1

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
