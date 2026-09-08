# Story manifest — decompose an outcome into an end-to-end story

Turn a customer outcome into an ordered set of modules, where each module advances the
customer toward the outcome and uses one product capability as the step that gets them
there. Record the story in the human-readable plan; maintain a machine-readable manifest
when an existing repository or tool workflow uses it. Every artifact (workshop, demo,
battlecard, survey, presentation) follows this story. The manifest is machine-readable
metadata; the complete deliverable is the repository of authored pages, code, scripts,
notebooks, decks and assets described in [repository.md](repository.md).

## The rule

Build the **journey**, then assign capabilities to its steps. Never the reverse. If you
start from "we have Skills, MCP, and Workflows, let's show each one," you have a feature
tour, not a story. Start from "the customer wants X; what is the path from where they are
today to X," and let capabilities fall onto the steps of that path.

## The fields

Plan new substantial curriculum through [intake.md](intake.md), then fill in
the story fields from the agreed brief. `assets/manifest-template.json` is an optional
machine-readable representation the agent can maintain. The plan and existing user answers
do not need another confirmation. Each core field earns its place:

- **use_case** — a one-line name for the journey, in the customer's words.
- **audience** — role + industry, and whether this is internal field or external customer.
- **outcome** — the value unlocked, stated as something the customer can *do* or *stop
  doing* afterward. "Cut entitlement-drift incidents to zero," not "use feature flags."
- **starting_point** — where they are today (stack, current workaround, the pain).
- **modules[]** — the ordered steps of the journey. Each module has:
  - **title** — the step, named by what the customer achieves in it.
  - **customer_value** — why this step matters to the outcome (one sentence).
  - **capability** — the single product capability this step leans on. One per module.
    If a module needs three capabilities, it is probably three modules.
  - **proof** — the concrete artifact that shows it worked: a passing test, a command and
    its output, a metric. This is what the verifier subagent will reproduce.
  - **status** — `draft` until verified, then `verified`.

## How to decompose

1. **Write the outcome as a before/after.** Before: the painful current state. After: the
   state once the value is unlocked. The story is the bridge between them.
2. **List the 3–6 steps** a customer actually takes to cross that bridge. Keep it to the
   real path; resist adding steps just to show a feature.
3. **Assign one capability per step.** Pick the minimal capability that advances the step.
   If a step needs no product capability, it is context, not a module.
4. **Name the proof for each step.** If you can't name an objective proof, the step is a
   claim, not a demonstration. Either find the proof or cut the step.
5. **Sanity check the arc.** Read the module titles in order with nothing else. Do they
   tell a story a customer would nod along to? If they read like a feature list, redo it.

## Example (abbreviated)

```
use_case: "A fintech platform team wants zero entitlement-drift incidents"
outcome:  "Catch and fix entitlement drift before it reaches production"
starting_point: "Drift is found by customers in prod; no automated check"

modules:
  1. title: "See the drift you can't see today"
     customer_value: "Surface mismatched entitlements across services"
     capability: "MCP grounding in the catalog of record"
     proof: "tool returns 2 drifted entitlements on the sample repo"
  2. title: "Encode the rule so it never regresses"
     customer_value: "Make the convention enforceable, not tribal knowledge"
     capability: "a Skill that captures the entitlement convention"
     proof: "skill flags a deliberately drifted entry in a new PR"
  3. title: "Run the check on every change"
     customer_value: "Catch drift in CI, not in prod"
     capability: "a scheduled routine / workflow audit"
     proof: "audit opens a draft PR; pytest passes after the fix"
```

Read those three titles alone: *see the drift, encode the rule, run the check.* That is a
story about reaching an outcome. The capabilities are the how, not the point.

## Presentation source

When a deck is requested, keep the slide story aligned with the modules and their actual
proofs. Read [presentation.md](presentation.md) for the workshop opening, teaching rhythm,
visual explanations, 40-word budget, notes, reveals and closing survey.

The optional story-manifest `presentation` object points to `storyboard_path`, nullable
`deck_path` and `qa_path`. It records source and deliverable locations; it does not prove
a deck exists or has passed checks. The starter uses `slides/presentation.json`, no deck
yet, and `slides/qa.md` for recorded checks. Older manifests may omit it.

This source metadata differs from canonical `workshop.json.presentation`, which contains
`workshopUrl`, `surveyUrl` and `slides`. Keep the actual storyboard at the path named in
the manifest and copy that definition into canonical JSON for Studio handoff. The
[presentation template](../assets/presentation-template.json) demonstrates that canonical
shape with no active URLs. Generated assets and rendered PPTX files are real repository/release files alongside the
metadata. Their absence is not satisfied by a populated JSON field.

## Repository and delivery metadata

Optional `planning`, `repository` and `delivery` fields record the saved plan, local/remote
source location, content host, exercise environment, feedback destination, access owners
and released source commit. The three destinations are chosen independently. See
[delivery.md](delivery.md) for their shapes; older manifests can omit them. Null records
an unresolved or not-yet-applicable value, never a deployed service or a completed check.
