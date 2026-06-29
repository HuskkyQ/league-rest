# Test Plan

## Test Strategy

Verify the MVP in layers, starting without the game:

- Unit tests for detector state transitions and coordinator behavior.
- Manual Windows checks using harmless substitute windows.
- Final manual check beside League of Legends only after substitute-window checks
  pass.

## Required Checks Per Task

Every development task must include:

- Success criteria with observable behavior.
- A verification command or manual checklist.
- A note when verification could not be run locally.

Every development task runs through this order:

1. Requirements Agent defines scope, assumptions, non-goals, success criteria,
   and verification.
2. UI Agent defines the minimum UI or interaction, including controls, labels,
   states, and manual user flow. It avoids speculative screens and does not write
   production code by default.
3. Implementation Agent implements exactly the assigned task.
4. Test Agent verifies behavior and adds focused tests when needed.
5. Code Review Agent reviews the final diff and reports findings first.

## Unit Tests

Planned unit coverage:

- Detector returns `alive`, `dead`, or `unknown` from fixture inputs.
- Detector threshold boundaries do not flip state unexpectedly.
- Detector returns `unknown` for missing samples, ambiguous samples, and samples
  too far from calibrated references.
- Coordinator switches to browser once for `alive -> dead`.
- Coordinator switches back once for `dead -> alive`.
- Coordinator does nothing for repeated states or `unknown`.
- Coordinator preserves the last confirmed `alive` or `dead` state across
  `unknown`, so noisy detector samples do not cause repeated focus switching.

## Manual Windows QA

Before testing with the game:

1. Use Notepad or another harmless app as the game-window substitute.
2. Use a normal browser window with a safe configured URL.
3. Trigger fake detector states or fixture-driven states.
4. Confirm focus changes happen once per state transition.
5. Confirm missing windows produce logs and no crash.

Beside the game:

1. Use a custom or practice environment only.
2. Confirm the utility observes the screen and window state only.
3. Confirm no gameplay input is sent.
4. Confirm focus returns only after the detector reports `alive`.

## Safety Verification

Review each implementation for prohibited approaches:

- No game memory reads or writes.
- No process injection.
- No anti-cheat bypass.
- No automated gameplay input.

Suggested documentation check:

```bash
rg -n "memory|inject|anti-cheat|gameplay automation|Windows|success criteria|Verification" docs
```
