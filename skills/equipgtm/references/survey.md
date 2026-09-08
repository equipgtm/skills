# Submission recipe — measure the outcome, then improve

A survey closes the loop. Its job is not to collect applause, it is to find out whether the
audience actually reached the outcome and what to fix next time. Build it from the same
manifest, so every question maps to the outcome or a module and every answer is something
you can act on. Learners explicitly submit their answers and any check results they
choose to share. EquipGTM Studio does not observe their private agent sessions, terminal
activity or local files.

## Choose the feedback destination

Resolve the form or submission store independently of the page host and exercise runtime,
using the destination already supplied in the plan. Keep question source and the mapping
to the external form in the workshop repository. Record the responsible owner, session
and release, submission URL and how authorized results will be exported for improvement.
Do not put raw learner answers in a public source repository. A survey definition or local
preview does not create a hosted collector. Use the verified destination for the closing
slide's readable URL and optional QR; see [presentation.md](presentation.md).

## What a good survey measures

- **Outcome confidence** — how confident learners feel about doing the outcome. Phrase it
  in the customer's words from the manifest `outcome`; confidence is not a verified pass.
- **Per-step clarity** — which module landed and which lost people. One question per module
  that earned it, not all of them.
- **The gap** — what was missing or confusing, in the learner's own words.
- **Intent** — the real win signal: would they run this on their own repo, or pilot it?
  Make it a clear yes / no / maybe, because that is the number you report back.
- **Willingness to recommend** — a single likelihood question.

## Authoring defaults

- Start with a short survey, usually **three to eight questions**. Customize the questions
  and order for the workshop and the instructor's research needs.
- **Every closed question must be actionable.** If an answer wouldn't change how you build
  or deliver next time, cut the question. A 1–5 on "how was the venue" teaches you nothing.
- Use open questions where the answer can change the next version; avoid repeating the
  same request for a comment after every module.
- Tie each per-step question to a real module title so you know exactly what to revise.

## Optional Studio survey format

For an external form destination, author the questions directly in its supported format
and keep source/mappings in the repository. Do not require a Studio import/export step.
The schema below applies when the task uses the EquipGTM Studio integration; the agent
handles the JSON behind the scenes.

Studio stores the customizable definition in `workshop.json` under `survey`. It includes
a `title`, `description` (which can be empty), and ordered `questions`. Every question
has a stable unique `id`, `type`, `label` and Boolean `required` flag. Use these types:

| Type | Definition | Submitted answer |
| --- | --- | --- |
| `short_text` | Short free-text prompt | String, at most 1,000 characters |
| `long_text` | Longer explanation | String, at most 10,000 characters |
| `single_choice` | `options`: 2–20 unique nonempty strings | One exact option string |
| `multiple_choice` | `options`: 2–20 unique nonempty strings | Array of unique option strings |
| `rating` | `scale`: `5` or `10` | Integer from 1 to the scale |

The current importer accepts 1–50 questions. IDs must start with a letter and contain
only letters, numbers, underscores or hyphens, up to 64 characters; reserved object names
are rejected. Keep IDs stable when clarifying wording. Give a materially different
question a new ID. Only choice questions accept `options`; only ratings accept `scale`.
Set rating scale explicitly when authoring, even though an omitted scale defaults to 5.

This is a survey definition suitable for the `survey` field or `equipgtm_set_survey`:

```json
{
  "title": "Diagnosing failed workflows — feedback",
  "description": "Help us improve the next workshop. Submit only what you want the instructor to receive.",
  "questions": [
    {"id": "outcome_confidence", "type": "rating", "required": true, "scale": 5,
     "label": "How confident are you diagnosing a failed workflow using its recorded events?"},
    {"id": "blockers", "type": "multiple_choice", "required": false,
     "label": "Which parts made it harder to complete the exercise?",
     "options": ["Environment setup", "Product access", "Exercise instructions", "Pacing"]},
    {"id": "gap", "type": "long_text", "required": false,
     "label": "What was missing or confusing?"},
    {"id": "pilot_intent", "type": "single_choice", "required": true,
     "label": "Would you try this workflow in a pilot?", "options": ["Yes", "No", "Maybe"]}
  ]
}
```

Write a readable `survey.md` when needed and adapt the definition to the customer's form
tool. Studio has no bundled live form-service integration. Keep module/outcome mappings
in the authoring notes keyed by question ID; `maps_to`, `text`, `open` and `scale_1_5`
are not canonical Studio question fields/types.

## Versioning and round-trip

The working draft's survey is editable. Saving a release freezes it with that release's
curriculum, and a session uses that snapshot. Editing the next draft must not change what
an earlier cohort was asked. Keep workshop/release, cohort and submission timestamps on
response records rather than adding them as unsupported survey-definition fields.

When using Studio interchange, export/import the embedded `workshop.json.survey` with
the curriculum. Changing only a sidecar does not update canonical JSON; the authoring
agent checks that IDs, choices, required flags and scales survive its round-trip. Older
workshop JSON without a survey uses the default definition for compatibility. For an
external form, check that form's published questions and version mapping instead.

For an available browser agent, use `equipgtm_set_survey` with the draft's current
`expectedUpdatedAt`, or import the complete canonical workshop. See
[studio-agent.md](studio-agent.md) for discovery, tool contracts and file fallback.

## Explicit check submissions

Give each checkpoint a module/check identifier and a short description of the expected
result. A submission can contain a learner-reported pass, failure or blocked state plus
an optional selected excerpt or artifact. Ask for only the output needed to interpret
the check; credentials and full private transcripts do not belong in the submission.

For an exported workshop, this is a portable record format, not an automatic collector:

```json
{
  "workshop_version": "1.0",
  "cohort_id": "<cohort identifier>",
  "module_id": "module-2",
  "check_id": "drift-detected",
  "submitted_at": "<ISO 8601 timestamp>",
  "result": "blocked",
  "evidence_source": "learner_reported",
  "evidence": "<optional excerpt selected by the learner>",
  "note": "<what prevented progress>"
}
```

Keep independent verifier evidence separately. A submitted screenshot or copied output
may help diagnose an issue, but receipt alone does not prove how it was produced. If the
instructor reproduces the check, record that additional evidence and its product version.

Local-mode submissions stay in that browser's localStorage. The hosted service
collects actual responses against a delivered session and its frozen survey. A local preview
does not prove shared delivery. Keep sample records and automated pilot responses labeled
as test data; do not describe them as customer feedback.

## After submissions arrive

Feed responses back into the manifest, which is what keeps the workspace from going stale:
low clarity on a module → revise that module; a "no" on pilot intent with a reason → fix
the story; a recurring gap → a missing module. The survey is the input to the next version,
not a vanity metric. Report the number of submissions alongside the cohort size when
available, and leave nonresponders as unknown. Use [refresh.md](refresh.md) to produce a
new version while retaining the version learners actually used.

Start analysis with question aggregates. Report rating distributions with their scale,
choice counts and the number of answers per question. For multiple-choice questions,
selection counts can exceed the number of respondents. Do not average unlike scales or
different question meanings across releases. Free-text answer content and individual
response records require the user's authorized scope; their presence in local storage
is not permission to send them to an agent or another service.
