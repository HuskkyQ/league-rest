# Sub-Agent Development Workflow

This project uses a five-role workflow for every development task.

## Assumptions

- Tasks are kept small enough for one implementation owner.
- Agents do not share hidden context; each prompt must include the task, file
  ownership, constraints, success criteria, and verification command.
- UI, implementation, and test ownership should be separated when practical.
- Review happens after tests, unless the implementation cannot be tested yet.

## Workflow

1. Requirements Agent: split the request.
   - Input: user request, `AGENTS.md`, relevant project docs, and current file
     list.
   - Output: task list with assumptions, non-goals, success criteria, and
     verification steps.
   - Verification: each task has a bounded scope and a clear done condition.

2. UI Agent: define the user interaction.
   - Input: task spec, `AGENTS.md`, and any existing UI docs or screenshots.
   - Output: the smallest required UI flow, controls, labels, states, and
     manual user flow.
   - Verification: the UI definition is bounded and does not add speculative
     screens or features.
   - Does not write production code by default.

3. Implementation Agent: implement one task.
   - Input: one task, assigned files, constraints, and verification steps.
   - Output: code changes plus a short summary of changed files.
   - Verification: run the task's listed checks before handing off.

4. Test Agent: verify behavior.
   - Input: task spec, implementation summary, changed files, and existing test
     commands.
   - Output: test changes if needed, test results, and any reproduction notes.
   - Verification: relevant tests pass or failures are documented precisely.

5. Code Review Agent: review the diff.
   - Input: task spec, changed files, and test results.
   - Output: findings first, then residual risk and a short summary.
   - Verification: no blocking findings remain.

## Handoff Rules

- The Requirements Agent may create or update task documents only.
- The UI Agent may create or update UI notes, wireframes, and interaction
  requirements only.
- The Implementation Agent may edit only assigned implementation files.
- The Test Agent may edit only assigned test files and minimal test fixtures.
- The Code Review Agent is read-only unless explicitly asked to prepare a patch.
- If a reviewer finds a blocking issue, the task returns to the Implementation
  Agent, then back through Test and Code Review.
- The controller runs the final verification command before declaring the task
  complete.

## Task Template

```markdown
## Task: <name>

Assumptions:
- <assumption>

Non-goals:
- <explicitly out of scope>

Implementation scope:
- Files allowed: <paths>
- Files not allowed: <paths or areas>

Success criteria:
- <observable result>

Verification:
- <command or manual check>
```
