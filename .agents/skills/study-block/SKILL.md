---
name: study-block
description: Research and teach one planned study block at the topic's saved depth, or answer a bounded course-concept question.
---

# Study a Block

Use this skill to research and teach one block from a saved study plan, or to
answer a bounded course-concept question. Broad topic research and map creation
belong to `study-plan`.

## Select the block and study depth

1. For a planned session, open the named `study/plans/<topic-slug>.md`. Read its
   topic-wide study depth, block scope, learning outcomes, and source references.
   If the user says to continue and exactly one unfinished plan exists, resume
   it; if several exist, ask which one. If no plan exists for a broad topic,
   direct the user to `study-plan` first.
2. Teach only the in-progress block or the single block explicitly requested.
   The saved study depth applies to the whole topic and every block; never set a
   separate depth for an individual block. A request to change the depth for a
   broad topic requires `study-plan` to revise the whole topic map first.

For a bounded question without a saved plan, use `medium` by default unless the
user gives a one-time depth preference. A one-time request changes that answer,
not the saved topic depth.

## Research the selected block before teaching

This skill owns the detailed source research for the selected block. Complete
the research pass before beginning the explanation:

1. Read the block's listed wiki topics, `OFF-NNN` and `EXT-NNN` sources, and
   any relevant references gathered during planning. Follow source citations
   to exact pages, sections, slides, or timestamps.
2. Search the repository for additional official or external material needed
   to meet the block's stated scope at the saved topic depth. Inspect originals
   when extracts omit important diagrams, formulas, tables, or context.
3. Synthesize the evidence, noting important assumptions, disagreements, and
   source gaps.

Apply the study-depth criteria in [`study-plan`](../study-plan/SKILL.md) to both
research and teaching.

Do not repeat topic-wide discovery for unrelated blocks. If research shows the
plan's scope or block sequence is materially incomplete, stop before teaching
the affected material and direct the user to `study-plan` to update the map.
If a student question reveals a factual gap during the block, research that
specific gap before answering; replan only if it changes topic-wide scope.

## Teach the researched block

Use the plan's scope and the research just completed. Follow `study.yaml` for
language, pacing, examples, and interaction preferences. A current user
instruction may change the response format without changing the saved depth.

Teach one manageable block at a time. Establish what problem the idea solves,
build intuition, then introduce terms and formalism. Ask numbered, open
questions and wait for the learner's reasoning unless they asked for a different
interaction style. Label invented scenarios as examples, not course material.

Explain source gaps plainly and cite important course claims. For PA examples
and PA-solving requests, follow the distinction in `AGENTS.md`; PA solving
belongs to `assignment-plan` or `assignment-step`.

## Update coverage

Update only the study plan's block statuses: mark the block covered when its
teaching and discussion are complete and no major confusion remains, then move
the in-progress status to the next block. Do not mark it covered while waiting
for an answer to an open question. Keep answers and learner profiles out of the
plan.

Close a completed block with its central idea and name the next block. After
the last planned block, ask integration questions spanning the
topic, then evaluate the learner's reasoning before marking the sequence
complete. Retain the completed plan.
