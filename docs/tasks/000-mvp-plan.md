# MVP Plan

Goal: build the smallest Windows utility that switches away from League of
Legends when the player's champion appears dead and switches back when the
champion appears alive again.

Reference docs:
- `docs/requirements.md`
- `docs/technical-approach.md`
- `docs/ui-interaction.md`
- `docs/test-plan.md`
- `docs/subagent-workflow.md`

## MVP Assumptions

- The first version uses screen-based or window-based signals only.
- The user will configure the browser target, such as a Douyin or Bilibili URL.
- The utility controls normal Windows focus switching only.
- Detection can start conservative and configurable before it is highly
  accurate.

## Non-Goals

- No game memory access.
- No process injection.
- No anti-cheat bypass.
- No gameplay automation.
- No macOS or Linux support.
- No browser feed automation beyond focusing an already opened page or launching
  a configured URL.

## Tasks

Each task must be handed to the next agent with assigned files, success
criteria, and verification. Keep each task small enough for one Implementation
Agent.

Each development task uses this order:
1. Requirements Agent
2. UI Agent
3. Implementation Agent
4. Test Agent
5. Code Review Agent

The UI Agent defines only the minimum UI or interaction for the task: controls,
labels, states, and manual user flow. It avoids speculative screens and does not
write production code by default.

### Task 1: Choose Minimal App Skeleton

Implementation scope:
- Add only the minimum project skeleton and run instructions needed for local
  execution.
- Do not implement detection or focus switching in this task.

Success criteria:
- Pick a Windows-friendly implementation stack.
- Document how to run the utility locally.
- Include one smoke check.

Verification:
- Run the chosen smoke check from a clean checkout.

### Task 2: Window Focus Switching Prototype

Implementation scope:
- Implement normal Windows window lookup and focus switching.
- Use a harmless substitute window for first verification.

Success criteria:
- Find the League of Legends game window by configurable title/process hint.
- Open or focus a configured browser URL.
- Switch focus back to the game window on command.

Verification:
- Manual Windows check with Notepad or another harmless app standing in for the
  game window.

### Task 3: Death And Respawn Signal Prototype

Implementation scope:
- Implement detector logic only.
- Use fixture inputs or screenshots for repeatable verification.

Success criteria:
- Implement a low-intrusion detector that can report `dead`, `alive`, or
  `unknown`.
- Keep detector thresholds configurable enough for manual calibration.
- Do not rely on memory reads or injected hooks.

Verification:
- Unit tests for detector state transitions using fixture inputs.

### Task 4: Coordinator Loop

Implementation scope:
- Connect detector states to focus switching.
- Do not add new detection methods in this task.

Success criteria:
- Poll detector state.
- Switch to browser once per death event.
- Switch back once per respawn event.
- Avoid repeated focus thrashing while the state is unchanged.

Verification:
- Unit tests for `alive -> dead -> alive` and `unknown` transitions.

### Task 5: Manual Windows QA Checklist

Implementation scope:
- Document the manual QA flow and expected logs.
- Do not change production behavior in this task.

Success criteria:
- Provide a checklist for running the utility beside League of Legends or a
  harmless window substitute.
- Include expected behavior, failure symptoms, and logs to collect.

Verification:
- Execute the checklist once with a substitute window before testing with the
  game.
- Checklist location: `docs/manual-windows-qa.md`.
