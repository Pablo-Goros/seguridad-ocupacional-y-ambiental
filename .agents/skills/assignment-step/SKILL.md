---
name: assignment-step
description: Execute exactly one fully specified step from a practical-assignment plan and explain the result.
---

# Assignment Step

This skill executes a saved plan. It does not collect assignment requirements,
research new approaches, expand the plan, or choose implementation details;
those belong to `assignment-plan`.

## Select the planned step

1. Read the named `assignment_plan.md` in the solution workspace. If the user
   says "next step" and exactly one unfinished plan exists, use it. If several
   plans exist, ask which assignment. If no plan exists, ask the user to create
   one with `assignment-plan`.
2. Select the explicitly requested pending step, or the first pending step
   whose dependencies are complete. If no steps remain, report that the plan is
   complete.
3. Before executing, confirm the step has its required inputs and references,
   is unblocked, and has no unresolved decision. If it is an explicit
   decision-gate, present its recorded options and recommendation, ask the user,
   record their choice in the gate, and stop. For any other gap or conflict,
   stop and have `assignment-plan` update the plan; do not fill gaps or choose
   an implementation option yourself.
4. Read the sources and workspace files referenced by that step. Do not repeat
   broad discovery or inspect unrelated assignments and course materials.

## Execute the planned step

Carry out the selected step as written in the solution workspace recorded by
its plan. Use its procedure, expected result, and checks. Do not add scope,
change the approach, reorder steps, or proceed to a later step.

Run the plan's test commands and compare the results with its acceptance
criteria. If a check fails, report the failure and leave the step in progress;
do not begin unplanned repair work.

After execution, update only this step's status and a concise outcome in the
plan. In your response, name the step, explain what changed, list the checks
and their results, and identify the next pending step. If the work is blocked
or partial, say what remains and stop for the user's next instruction.