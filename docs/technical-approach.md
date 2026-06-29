# Technical Approach

## Shape

Use the smallest Windows desktop utility that can coordinate three pieces:

- Window lookup: find the game window and browser window using normal Windows
  APIs and configurable hints.
- Detector: inspect screen or window-derived signals and return `alive`, `dead`,
  or `unknown`.
- Coordinator: react to state transitions and perform normal focus switching.

## Detection Approach

Start with a low-intrusion detector:

- Capture a configured screen or game-window region.
- Compare simple visual indicators, such as grayscale/death overlay, respawn UI,
  or a calibrated region near the champion HUD.
- Return `unknown` when the window is missing, minimized, covered, or the signal
  is below threshold.

The detector must not use game memory, injected hooks, anti-cheat bypasses, or
gameplay automation.

## Focus Switching

- Find the League of Legends window by configured title or process hint.
- Focus an existing browser window when possible.
- Open the configured URL only when no matching browser window is available.
- Return focus to the game only after an observed `dead -> alive` transition.
- Debounce state changes so the same state does not trigger repeated switching.

## Minimal Configuration

Keep configuration small:

- Game window title or process hint.
- Browser URL.
- Optional browser window title hint.
- Detector region selected during calibration.

Keep detector thresholds calibration-derived and keep poll interval internal for
the MVP. Do not expose raw tuning controls unless later testing proves they are
needed.

Avoid speculative plugin systems, profiles, or remote configuration until the MVP
needs them.

## Logging

Log only operational events needed for local debugging:

- Window match results.
- Detector state changes.
- Focus actions.
- Reasons for `unknown`.

Do not log personal browser content or game account information.
