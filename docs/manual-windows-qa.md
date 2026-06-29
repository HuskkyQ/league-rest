# Manual Windows QA Checklist

Use this checklist after automated tests pass. Start with harmless substitute
windows before testing beside League of Legends.

## Prerequisites

- Windows with Python installed.
- `league-rest` installed from source or from the release wheel.
- A normal browser installed and available as the default browser.
- League of Legends in windowed or borderless windowed mode for final checks.

Verify the install:

```powershell
league-rest --smoke
python -m pytest
```

Expected smoke output:

```text
league-rest smoke ok
```

## Substitute-Window Check

1. Open Notepad.
2. Open a browser window.
3. Run:

   ```powershell
   league-rest windows
   ```

4. Confirm the output includes a Notepad-like window and the browser window.
5. Run:

   ```powershell
   league-rest open-browser --url "https://www.bilibili.com"
   ```

6. Confirm the browser opens or focuses the URL.
7. Run:

   ```powershell
   league-rest focus-game --title "Notepad"
   ```

8. Confirm focus returns to Notepad.

## Detector And Coordinator Logic Check

Run:

```powershell
python -m pytest tests/test_detector.py tests/test_coordinator.py
```

Expected result:

- Detector fixture tests pass for `alive`, `dead`, `unknown`, ambiguous input,
  missing input, and threshold boundaries.
- Coordinator tests pass for `alive -> dead -> alive`, repeated states, and
  `unknown` transitions.

## League-Side Check

Only run this after the substitute-window check passes.

1. Start League of Legends in a practice/custom environment.
2. Use windowed or borderless windowed mode.
3. Run:

   ```powershell
   league-rest windows
   ```

4. Identify the title or process hint for the game window.
5. Run:

   ```powershell
   league-rest focus-game --title "League of Legends"
   ```

6. Confirm normal Windows focus returns to the game window.

## Expected Limitations

- This build does not capture screenshots.
- This build does not automatically detect real in-game death or respawn.
- This build does not run a background loop.
- This build does not provide tray UI or a settings window.
- Exclusive fullscreen may block normal Windows focus behavior.

## Failure Notes To Collect

- Command that failed.
- Full terminal output.
- Windows version.
- Python version from `python --version`.
- Whether League was windowed, borderless, or exclusive fullscreen.
- Window titles shown by `league-rest windows`.
