# UI Interaction

## MVP UI Shape

Use a tray app plus one small settings/status window.

Reasons:
- The utility should run in the background while the user plays or browses.
- A tray menu is enough for quick `Start`, `Pause`, and `Exit` actions.
- A small window is still needed for first-time setup and detector calibration.
- A full multi-page app would add scope without improving the MVP.

## Required Controls

Keep the window to the minimum controls needed:

- `Game window hint`: text input for matching the game window.
- `Browser URL`: text input for the page to open or focus.
- `Browser window hint`: optional text input for preferring an existing browser
  window.
- `Detection region`: read-only display of the selected region.
- `Set region`: button that starts region selection.
- `Calibrate alive`: button that samples the selected region while alive.
- `Calibrate dead`: button that samples the selected region while dead.
- `Start/Pause`: button that controls the detector loop.
- `Recent events`: short read-only event list or an `Open log` button.

Do not expose poll interval, raw thresholds, or model parameters in the MVP. If
manual tuning is necessary, use one `Sensitivity` control with
`Conservative`, `Normal`, and `Aggressive`, defaulting to `Normal`.

## States

Show the same state in the tray tooltip and at the top of the window:

- `Paused`: detection is stopped.
- `Running: alive`: detection is active and the player appears alive.
- `Running: dead`: detection is active and the player appears dead.
- `Running: unknown`: detection is active but the signal is not reliable.
- `Error`: required configuration or normal window focus action failed.

Recent events should include only local operational messages, such as:

- `Matched game window`
- `State changed: alive -> dead`
- `Focused browser`
- `State changed: dead -> alive`
- `Focused game`
- `Unknown: game window not found`

## Calibration Flow

1. Open League of Legends and make the relevant HUD or death indicator visible.
2. Click `Set region`.
3. Select one stable screen region.
4. Click `Calibrate alive` while the champion is alive.
5. Click `Calibrate dead` while the champion is dead.
6. Let the utility calculate the threshold from the two samples.
7. Click `Start`.

Calibration errors should stay simple:

- `Alive/dead samples are too similar. Choose a clearer region.`
- `Game window not visible. Bring the game to front and try again.`

## UI Non-Goals

- No landing page or marketing screen.
- No account system, login, cloud sync, telemetry, or updater UI.
- No content recommendation UI.
- No browser controls such as scroll, like, or autoplay controls.
- No complex settings page, profile system, or raw vision tuning panel.
- No in-game overlay.
- No controls that automate gameplay input.
