# Requirements

## Goal

Build a small Windows-only utility that watches whether the player's League of
Legends champion appears dead, focuses a configured browser page while dead, and
focuses the game again when the champion appears alive.

## MVP Assumptions

- The MVP runs on Windows only.
- The first detector uses screen observation, window titles, process names, or
  other normal desktop signals.
- The user can configure the game window hint and browser target.
- Detection may report `unknown` when the signal is not reliable.
- The first version prefers conservative behavior over aggressive switching.

## Functional Requirements

- Detect the candidate League of Legends game window from a configurable title or
  process hint.
- Detect a simple champion state: `alive`, `dead`, or `unknown`.
- Focus or open a configured browser URL when the state changes to `dead`.
- Focus the game window when the state changes from `dead` to `alive`.
- Avoid repeated focus switching while the detected state is unchanged.
- Provide visible logs for state changes and focus actions.

## Safety Requirements

- Do not read or modify game memory.
- Do not inject into the game process.
- Do not bypass anti-cheat systems.
- Do not automate gameplay actions.
- Use normal Windows focus switching only.

## Non-Goals

- No macOS or Linux support in the MVP.
- No game input automation, including clicks, key presses, or ability usage.
- No browser feed control beyond focusing an existing page or opening a
  configured URL.
- No cloud service, account system, telemetry, or updater.
- No high-accuracy computer vision model in the first pass.

## Done Criteria

- Each implementation task has success criteria and verification steps.
- Each development task follows the five-role order: Requirements Agent, UI
  Agent, Implementation Agent, Test Agent, Code Review Agent.
- UI Agent work is limited to the minimum UI flow, controls, labels, states, and
  manual user flow needed for the task.
- The MVP can be tested with harmless substitute windows before testing beside
  the game.
- The utility never requires memory access, injection, anti-cheat bypass, or
  gameplay automation to satisfy MVP behavior.
