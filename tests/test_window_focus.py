import pytest
import subprocess
import sys
from ctypes import wintypes

from league_rest.window_focus import (
    BrowserTarget,
    FakeWindowController,
    UnsupportedPlatformError,
    WindowInfo,
    WindowTarget,
    _configure_kernel32,
    _configure_user32,
    focus_browser,
    focus_game,
)


def test_focus_game_matches_title_hint():
    controller = FakeWindowController(
        [
            WindowInfo(handle=1, title="Untitled - Notepad", process_name="notepad.exe", pid=100),
            WindowInfo(handle=2, title="League of Legends", process_name="LeagueClientUx.exe", pid=200),
        ]
    )

    matched = focus_game(WindowTarget(title_hint="league"), controller)

    assert matched.handle == 2
    assert controller.focused_handles == [2]


def test_focus_game_matches_process_hint():
    controller = FakeWindowController(
        [
            WindowInfo(handle=1, title="Untitled - Notepad", process_name="notepad.exe", pid=100),
            WindowInfo(handle=2, title="Game Window", process_name="LeagueClientUx.exe", pid=200),
        ]
    )

    matched = focus_game(WindowTarget(process_hint="leagueclient"), controller)

    assert matched.handle == 2
    assert controller.focused_handles == [2]


def test_focus_game_reports_missing_window():
    controller = FakeWindowController([])

    with pytest.raises(LookupError, match="No matching game window"):
        focus_game(WindowTarget(title_hint="League of Legends"), controller)


def test_focus_browser_opens_url_when_no_browser_hint():
    controller = FakeWindowController([])

    focused = focus_browser(BrowserTarget(url="https://www.bilibili.com"), controller)

    assert focused is None
    assert controller.opened_urls == ["https://www.bilibili.com"]
    assert controller.focused_handles == []


def test_focus_browser_focuses_existing_browser_before_opening_url():
    controller = FakeWindowController(
        [
            WindowInfo(handle=7, title="Bilibili - Chrome", process_name="chrome.exe", pid=700),
        ]
    )

    focused = focus_browser(
        BrowserTarget(url="https://www.bilibili.com", window_hint="bilibili"),
        controller,
    )

    assert focused is not None
    assert focused.handle == 7
    assert controller.focused_handles == [7]
    assert controller.opened_urls == []


def test_real_controller_is_windows_only_on_non_windows():
    if pytest.importorskip("sys").platform == "win32":
        pytest.skip("non-Windows behavior only")

    from league_rest.window_focus import WindowsWindowController

    with pytest.raises(UnsupportedPlatformError):
        WindowsWindowController()


def test_window_command_reports_unsupported_platform_on_non_windows():
    if sys.platform == "win32":
        pytest.skip("non-Windows behavior only")

    result = subprocess.run(
        [sys.executable, "-m", "league_rest", "windows"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 2
    assert "only supported on Windows" in result.stderr
    assert "Traceback" not in result.stderr


class _FunctionStub:
    pass


class _LibraryStub:
    def __init__(self, names):
        for name in names:
            setattr(self, name, _FunctionStub())


def test_win32_function_signatures_are_declared():
    user32 = _LibraryStub(
        [
            "EnumWindows",
            "IsWindowVisible",
            "GetWindowTextLengthW",
            "GetWindowTextW",
            "GetWindowThreadProcessId",
            "ShowWindow",
            "SetForegroundWindow",
        ]
    )
    kernel32 = _LibraryStub(["OpenProcess", "QueryFullProcessImageNameW", "CloseHandle"])

    _configure_user32(user32)
    _configure_kernel32(kernel32)

    assert user32.SetForegroundWindow.argtypes == [wintypes.HWND]
    assert user32.SetForegroundWindow.restype == wintypes.BOOL
    assert kernel32.OpenProcess.restype == wintypes.HANDLE
    assert kernel32.QueryFullProcessImageNameW.argtypes[0] == wintypes.HANDLE
    assert kernel32.CloseHandle.argtypes == [wintypes.HANDLE]
