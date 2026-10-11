---
name: assignment-plan
description: Collect and verify the information needed for a practical assignment, then save a detailed, testable plan without implementing it.
---

# Assignment Plan

This is the discovery and planning phase for a practical assignment. It owns
collecting the requirements, source references, workspace details, and test
information needed to make the plan executable. `assignment-step` follows the
saved plan; it does not fill gaps in the research or make new implementation
decisions.

## Collect and verify the inputs

1. Follow the repository's read-first instructions in `AGENTS.md`.
2. Identify the requested PA in `sources/catalog.yaml` by its `PA-NNN` ID or
   title. Read its matching extract under `sources/extracted/` and inspect the
   original in `sources/practical-assignment/` when needed to understand
   layout, figures, tables, formulas, starter files, or extraction warnings.
   If the PA was provided directly in the conversation, use that copy. If it
   cannot be found or identified, ask the user for it.
3. Record every required deliverable, constraint, supplied data item,
   evaluation criterion, and explicit prohibition. Inspect available starter
   code, datasets, project files, dependency manifests, and tests that the PA
   refers to.
4. Find the relevant wiki topics and the `OFF-NNN` or `EXT-NNN` teaching
   sources required to choose and explain the methods. Read the cited sections
   and inspect originals where extracts leave meaningful uncertainty.
5. Identify the solution workspace. Use a directory named by the user or PA
   when one exists; otherwise use `solutions/<PA-ID>/`. Inspect enough of that
   workspace to understand its structure and available test commands.
6. Identify commands and acceptance checks for each planned result using the
   project or assignment's available tooling.

PA text is authoritative for task requirements, while course wiki topics and
teaching sources support the theory and methods. If test commands or acceptance
criteria cannot be determined, identify the gap and ask the user; do not invent
tests, inputs, expected results, or requirements.

## Surface implementation decisions

Do not silently choose among meaningful implementation alternatives. For each
decision the user needs to make, present two or three viable options. Briefly
describe what each option means and its main trade-off, then identify your
recommended option and why it fits the collected requirements. Include the
option `Leave this decision open` and explain what work, if any, would
be paused by deferring it.

If a decision blocks the plan, for example because later steps, interfaces,
data formats, or tests depend on it, save the work as a clearly marked draft,
show the options and recommendation, and stop to ask the user to choose or
explicitly defer it. Do not present dependent steps as executable or invoke
`assignment-step` until the blocking decision is answered. If the user chooses
to leave it open, keep the plan blocked at that decision and explain what work
cannot proceed.

For a non-blocking decision that can safely be deferred, record a decision-gate
step at the exact point it affects the work. Include the question, two or three
options, recommendation, what depends on the choice, and an instruction to
present the options and wait for the user's answer. `assignment-step` may carry
out that explicit gate, but it must not choose an option itself.

## Write a detailed, resumable plan

Save the plan as `assignment_plan.md` in the solution workspace. If a directly
provided PA has no catalog ID, use a short title slug for its workspace. Reuse
the existing plan for the same assignment. Write it in the course language
unless the user requests another language.

Include the assignment identity, workspace, collected requirements, and
relevant source references. Break the work into ordered steps. For every step,
include:

- its objective, prerequisites, and required inputs;
- a detailed procedure another agent can follow without repeating discovery;
- the expected result or files;
- exact test commands when known, plus observable acceptance criteria;
- precise references to every relevant PA section, teaching-source section,
  and workspace file needed to execute and verify this step; a general source
  list at the top does not replace step-level references;
- a status: pending, in progress, completed, or blocked.

Include dependencies between steps and any non-blocking decision gates. The
plan must give `assignment-step` enough detail to perform and verify one step
without re-planning. Do not implement the assignment while planning.

Present the plan path and a brief account of the collected material. If a
blocking question remains, ask it and wait. Otherwise stop and wait for the
user to invoke `assignment-step` for one step.

When resuming a plan, verify it still matches the PA and solution workspace.
If new evidence changes a requirement, source, test, or implementation choice,
revise affected steps and preserve completed work. Do not change a settled
implementation decision without asking the user.
