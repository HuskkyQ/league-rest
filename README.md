# league-rest

Minimal Python CLI skeleton for a Windows-only League of Legends rest utility.

The current prototype includes smoke checks and manual Windows window focus
commands plus fixture-based detector logic. It does not implement real screenshot
capture, real game-state detection, tray UI, or automatic switching loops yet.

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

## Detector Fixture Prototype

The detector prototype is pure logic. It compares fixture feature vectors against
calibrated `alive` and `dead` reference samples and returns `alive`, `dead`, or
`unknown`.

This prototype does not capture screenshots, read image files, run OCR or ML, or
connect to League of Legends. Screenshot capture and calibration UI are later
MVP work.

## Coordinator Prototype

The coordinator prototype connects detector states to focus actions without
running a background service. It calls browser focus once when state changes to
`dead`, calls game focus once when state changes from `dead` to `alive`, and
does nothing for repeated states or `unknown`.

It is currently covered by unit tests with fake focus actions. It does not poll
the screen, run as a daemon, or provide pause/status UI yet.

## Manual Windows QA

Use [docs/manual-windows-qa.md](docs/manual-windows-qa.md) to verify the release
on Windows. Run the substitute-window check before testing beside League of
Legends.
