# AGENTS.md

Behavioral guidelines for this project. Follow these instructions together with
the active task request.

## Project Goal

Build a simple Windows-only utility for League of Legends that:

- Detects when the player's champion appears to be dead.
- Switches focus to a configured browser page, such as Douyin or Bilibili.
- Switches focus back to the game when the champion appears to be alive again.

## Safety And Scope

- Prefer low-intrusion approaches: screen observation, window title/process
  detection, configurable hotkeys, and normal Windows focus switching.
- Do not read or modify game memory.
- Do not inject into the game process.
- Do not bypass anti-cheat systems.
- Do not automate gameplay actions.
- Keep the first version Windows-only.

## Development Principles

- State assumptions before implementation when the task has multiple plausible
  interpretations.
- Ask when uncertainty blocks a safe implementation.
- Prefer the minimum code that solves the current task.
- Do not add speculative features, abstractions, or configuration.
- Touch only files required by the task.
- Match existing style once code exists.
- Remove only unused code created by the current change.
- Every task must have explicit verification before it is considered done.

## Required Sub-Agent Workflow

Every development task follows this sequence:

1. Requirements Agent
   - Reads the user request and existing project docs.
   - Splits the request into small implementation tasks.
   - Defines assumptions, non-goals, success criteria, and verification.
   - Does not write production code.

2. UI Agent
   - Defines the smallest UI or interaction needed for the task.
   - Specifies controls, labels, states, and manual user flow when UI is in
     scope.
   - Keeps UI requirements practical and avoids speculative screens.
   - Does not write production code unless explicitly assigned a UI
     implementation task.

3. Implementation Agent
   - Implements exactly one approved task.
   - Owns only the files assigned for that task.
   - Does not expand scope or refactor unrelated code.
   - Runs the task-level verification it can run locally.

4. Test Agent
   - Reviews the implemented behavior against the task success criteria.
   - Adds or updates focused tests when the task requires tests.
   - Runs relevant tests and reports failures with reproduction steps.

5. Code Review Agent
   - Reviews the final diff for correctness, maintainability, scope control, and
     missing verification.
   - Leads with findings ordered by severity.
   - Does not replace test execution.

The controller only marks a task complete when implementation, testing, and code
review have no blocking issues.
