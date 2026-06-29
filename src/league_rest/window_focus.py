from __future__ import annotations

from dataclasses import dataclass
import ctypes
from ctypes import wintypes
import os
import platform
from typing import Optional, Union
import webbrowser


class UnsupportedPlatformError(RuntimeError):
    pass


@dataclass(frozen=True)
class WindowInfo:
    handle: int
    title: str
    process_name: str
    pid: int


@dataclass(frozen=True)
class WindowTarget:
    title_hint: Optional[str] = None
    process_hint: Optional[str] = None


@dataclass(frozen=True)
class BrowserTarget:
    url: str
    window_hint: Optional[str] = None


class FakeWindowController:
    def __init__(self, windows: list[WindowInfo]):
        self._windows = windows
        self.focused_handles: list[int] = []
        self.opened_urls: list[str] = []

    def list_windows(self) -> list[WindowInfo]:
        return list(self._windows)

    def focus_window(self, handle: int) -> None:
        self.focused_handles.append(handle)

    def open_url(self, url: str) -> None:
        self.opened_urls.append(url)


class WindowsWindowController:
    def __init__(self) -> None:
        if platform.system() != "Windows":
            raise UnsupportedPlatformError("Window focus is only supported on Windows")
        self._user32 = ctypes.windll.user32
        self._kernel32 = ctypes.windll.kernel32
        _configure_user32(self._user32)

    def list_windows(self) -> list[WindowInfo]:
        windows: list[WindowInfo] = []

        enum_proc_type = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

        def enum_proc(hwnd: int, _lparam: int) -> bool:
            if not self._user32.IsWindowVisible(hwnd):
                return True

            length = self._user32.GetWindowTextLengthW(hwnd)
            if length == 0:
                return True

            buffer = ctypes.create_unicode_buffer(length + 1)
            self._user32.GetWindowTextW(hwnd, buffer, length + 1)
            title = buffer.value.strip()
            if not title:
                return True

            pid = wintypes.DWORD()
            self._user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            windows.append(
                WindowInfo(
                    handle=int(hwnd),
                    title=title,
                    process_name=_process_name_from_pid(int(pid.value)),
                    pid=int(pid.value),
                )
            )
            return True

        self._user32.EnumWindows(enum_proc_type(enum_proc), 0)
        return windows

    def focus_window(self, handle: int) -> None:
        self._user32.ShowWindow(handle, 9)
        self._user32.SetForegroundWindow(handle)

    def open_url(self, url: str) -> None:
        webbrowser.open(url, new=2)


WindowController = Union[FakeWindowController, WindowsWindowController]


def focus_game(target: WindowTarget, controller: WindowController) -> WindowInfo:
    window = _find_window(target, controller.list_windows())
    if window is None:
        raise LookupError("No matching game window")
    controller.focus_window(window.handle)
    return window


def focus_browser(
    target: BrowserTarget,
    controller: WindowController,
) -> Optional[WindowInfo]:
    if target.window_hint:
        window = _find_window(WindowTarget(title_hint=target.window_hint), controller.list_windows())
        if window is not None:
            controller.focus_window(window.handle)
            return window

    controller.open_url(target.url)
    return None


def _find_window(target: WindowTarget, windows: list[WindowInfo]) -> Optional[WindowInfo]:
    title_hint = target.title_hint.lower() if target.title_hint else None
    process_hint = target.process_hint.lower() if target.process_hint else None

    for window in windows:
        title = window.title.lower()
        process_name = window.process_name.lower()
        if title_hint and title_hint in title:
            return window
        if process_hint and process_hint in process_name:
            return window

    return None


def _process_name_from_pid(pid: int) -> str:
    if platform.system() != "Windows":
        return str(pid)

    _configure_kernel32(ctypes.windll.kernel32)
    process_query_limited_information = 0x1000
    kernel32 = ctypes.windll.kernel32
    handle = kernel32.OpenProcess(process_query_limited_information, False, pid)
    if not handle:
        return str(pid)

    try:
        size = wintypes.DWORD(260)
        buffer = ctypes.create_unicode_buffer(size.value)
        if kernel32.QueryFullProcessImageNameW(handle, 0, buffer, ctypes.byref(size)):
            return os.path.basename(buffer.value)
        return str(pid)
    finally:
        kernel32.CloseHandle(handle)


def _configure_user32(user32) -> None:
    user32.EnumWindows.argtypes = [
        _windows_callback_type()(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM),
        wintypes.LPARAM,
    ]
    user32.EnumWindows.restype = wintypes.BOOL
    user32.IsWindowVisible.argtypes = [wintypes.HWND]
    user32.IsWindowVisible.restype = wintypes.BOOL
    user32.GetWindowTextLengthW.argtypes = [wintypes.HWND]
    user32.GetWindowTextLengthW.restype = ctypes.c_int
    user32.GetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
    user32.GetWindowTextW.restype = ctypes.c_int
    user32.GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
    user32.GetWindowThreadProcessId.restype = wintypes.DWORD
    user32.ShowWindow.argtypes = [wintypes.HWND, ctypes.c_int]
    user32.ShowWindow.restype = wintypes.BOOL
    user32.SetForegroundWindow.argtypes = [wintypes.HWND]
    user32.SetForegroundWindow.restype = wintypes.BOOL


def _configure_kernel32(kernel32) -> None:
    kernel32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    kernel32.OpenProcess.restype = wintypes.HANDLE
    kernel32.QueryFullProcessImageNameW.argtypes = [
        wintypes.HANDLE,
        wintypes.DWORD,
        wintypes.LPWSTR,
        ctypes.POINTER(wintypes.DWORD),
    ]
    kernel32.QueryFullProcessImageNameW.restype = wintypes.BOOL
    kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel32.CloseHandle.restype = wintypes.BOOL


def _windows_callback_type():
    return getattr(ctypes, "WINFUNCTYPE", ctypes.CFUNCTYPE)
