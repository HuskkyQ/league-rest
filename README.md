# league-rest

Minimal Python CLI skeleton for a Windows-only League of Legends rest utility.

This task does not implement champion state detection, window lookup, focus
switching, tray UI, screenshots, or browser control.

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
python -m pytest tests/test_smoke.py
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
