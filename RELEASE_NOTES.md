# league-rest 0.1.0

Initial release.

## Install On Windows

Download `league_rest-0.1.0-py3-none-any.whl` from this release, then run:

```powershell
py -m pip install .\league_rest-0.1.0-py3-none-any.whl
league-rest --smoke
```

Expected output:

```text
league-rest smoke ok
```

## Included

- Minimal Python CLI package skeleton.
- `league-rest` console command.
- Smoke check for installation verification.
- Project requirements, technical approach, UI boundary, and test plan docs.

## Not Included Yet

- League of Legends window detection.
- Browser or game focus switching.
- Death/respawn detection.
- Tray app or settings window.
- Standalone `.exe` or `.msi` installer.

This release is a Python wheel. It is installable on Windows when Python is
available, but it is not a standalone Windows installer.
