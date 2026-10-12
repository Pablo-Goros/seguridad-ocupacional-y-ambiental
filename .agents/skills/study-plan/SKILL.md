---
name: study-plan
description: Research a course topic and create a saved study map at the requested topic-wide depth, without teaching its blocks.
---

# Study Plan

Use this skill to research and plan a broad topic before teaching begins. It
owns topic-level research and creates the depth-specific map used by
`study-block`. Do not teach a block in this workflow.

## Choose the study depth

Accept a topic-wide study depth in the request, for example:
`$study-plan Dark matter, heavy`. The available study-depth levels are `light`,
`medium`, and `heavy`. A new plan defaults to `medium` when no depth is given.
When resuming an existing plan without asking to change its study depth,
preserve the saved level. If an existing plan has no saved depth, add `medium`.

Store exactly one study-depth level for the topic in the plan metadata. Do not
assign separate levels to individual blocks. The study depth sets the expected
coverage of every block:

- `light`: a high-level, superficial understanding. Focus on the central
  question, intuition, essential terms, and main relationships. Use a simple
  example; omit technical detail unless needed to understand the core idea.
- `medium`: a solid understanding, closer to heavy than light. Cover the core
  mechanisms and formal ideas, key assumptions, worked examples, relationships,
  important limitations, and common confusions. Leave specialized derivations,
  rare variants, and edge cases for heavy unless they are central to the course.
- `heavy`: aim for comprehensive understanding within the topic's scope and
  available evidence. Plan for relevant formal details and derivations, proof or
  algorithm steps where applicable, assumptions, variants, edge cases,
  applications, limitations, comparisons, misconceptions, and connections to
  prerequisites. Do not claim to cover every fact ever published on a broad
  field; identify where available sources leave gaps.

Normally preserve the same major block sequence across study depths. Change the
scope, subtopics, outcomes, source coverage, and planned detail within each
block to match the topic-wide study depth. Add or remove a major block only when
the research shows that the topic structure requires it.

## Research the topic and build the map

1. Follow the repository's read-first instructions in `AGENTS.md`, then search
   the wiki by topic name, aliases, related concepts, and prerequisites.
   Read the relevant topics, then locate matching `OFF-NNN` and `EXT-NNN`
   entries in `sources/catalog.yaml` and their extracts. Inspect original
   sources when extracts omit meaningful diagrams, formulas, tables, or
   context.
2. Research the topic across its relevant course materials deeply enough to
   determine the blocks and their coverage at the selected depth. At `heavy`,
   survey all relevant teaching sources found in the repository, not just the
   wiki summaries. At `light`, prioritize the central sources and overview.
3. Order blocks from prerequisites to dependent ideas. For each block, prepare
   a clear scope, learning outcomes, key concepts or questions, and precise
   source references. This is a researched teaching outline, not a full lesson.

If repository sources do not support the requested depth, identify the gap in
the plan rather than inventing coverage.

Save or update `study/<topic-slug>.md`, using
[`study_template.md`](study_template.md) as a structure. Write plan content in
the course language unless the user requests another language; keep the study
depth value itself as the canonical English word `light`, `medium`, or `heavy`.
Include the topic, its single study-depth level, and ordered blocks with a
status, scope, learning outcomes, and source references. Add detail to each
block's research outline according to the selected depth. Do not store student
answers, demonstrated understanding, misconceptions, or learner profiles.

Create the output directory if needed. Discover saved plans in `study/`.
For compatibility, also check root-level `study_<topic-slug>.md` plans: when
resuming one, move it to the new path without changing its depth, content, or
statuses. If both paths exist for the same topic, compare them and resolve
which to resume without overwriting either silently. Fix relative links when
moving a plan; links to repository sources must resolve from `study/`.

For a new plan, mark the first block in progress and the rest pending. Preserve
statuses when resuming if the block scope has not changed. When the study depth
changes, revise the research outline for the whole topic and reset coverage
only for blocks whose planned scope has changed.

If the topic is not named and exactly one unfinished plan exists, resume it;
if several exist, ask which one. Do not replace an existing map unless the user
asks or the research shows it no longer fits the topic.

Present the saved path and map, state the selected study depth, and stop. Direct
the user to `study-block` to begin or continue a block. For a bounded one-off
question, use `study-block` without requiring a multi-block plan.
