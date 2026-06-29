# league-rest

Minimal Python CLI skeleton for a Windows-only League of Legends rest utility.

The current prototype includes smoke checks and manual Windows window focus
commands. It does not implement champion state detection, tray UI, screenshots,
or automatic switching loops yet.

## Safety Boundaries

- Does not read or modify game memory.
- Does not inject into the game process.
- Does not bypass anti-cheat systems.
- Does not automate gameplay actions.

## Development Setup

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e .
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .
```

## Test Setup

```powershell
python -m pip install -e ".[dev]"
python -m pytest
```

## Smoke Check

```bash
python -m league_rest --smoke
```

Expected output includes:

```text
league-rest smoke ok
```

## Install From A GitHub Release On Windows

Download `league_rest-0.1.0-py3-none-any.whl` from the GitHub Release, then run:

```powershell
py -m pip install .\league_rest-0.1.0-py3-none-any.whl
league-rest --smoke
```

This wheel is a Python package that installs a `league-rest` console command.
It is not a standalone `.exe` or `.msi` installer.

## Window Focus Prototype

These commands are Windows-only and use normal desktop window lookup and focus
switching. They do not read game memory, inject into the game process, bypass
anti-cheat systems, or automate gameplay input.

List visible windows:

```powershell
league-rest windows
```

Open or focus a browser URL:

```powershell
league-rest open-browser --url "https://www.bilibili.com"
```

Focus a game or substitute window by title:

```powershell
league-rest focus-game --title "League of Legends"
```

For first verification, use a harmless substitute such as Notepad before testing
beside League of Legends. Windowed or borderless windowed mode is recommended;
exclusive fullscreen may prevent normal Windows focus switching.
