# Improve recipe — refresh a workshop from evidence

The promise of EquipGTM is that you come back to a use-case workspace and update it as the
product evolves, instead of rebuilding from a blank session. This recipe is that loop: given
a product change (a release, a new feature, a changelog) or fresh feedback, find what the
change touches, update only that, and re-verify.

This runs on an **existing** workspace, not a fresh build. The instructor chooses the
change to investigate and uses their own agent to make the revision. The local UI can
organize records; it does not monitor the product or observe learner sessions.

## When to run it

- The product shipped something: a new feature, a renamed capability, a changed flow.
- An explicitly submitted survey/check result or a facilitator note surfaced a weak module.
- Time has passed and you're not sure what's stale.

## The flow

1. **Take the change and the existing manifest(s).** Read the supplied changelog, diff or
   feedback. Identify the workshop version, product version and cohort the evidence
   concerns. Keep learner-reported results distinct from independently reproduced checks.
2. **Map the change to the stories.** For each change, ask: does it *break* a module's claim,
   *strengthen* it, or *enable a new use case*? A new use case is a new workspace (run
   intake); the rest are updates here.
3. **Update only what's affected.** Outcomes are stable; modules change. Update the
   affected pages and their exercise code, example scripts, notebooks, presentation source,
   assets and dependency files together. Updating JSON alone does not update those files.
   Leave unrelated material intact.
4. **Re-verify the touched claims.** Run the verifier subagent on the affected modules and
   any dependent steps, re-running proofs against the intended product version. Shared
   setup or access changes may affect the whole workshop. Save actual results.
5. **Re-render and record.** Create the next workshop version, rebuild the affected
   artifacts, and record the reason and evidence for each change. Record the source Git
   commit and archive checksums for the next delivery; retain the earlier cohort's frozen
   artifacts even as the working branch advances. Regenerate the learner
   bundle and tutor guidance when their content changed. Keep delivered versions available
   so an existing cohort's instructions and submissions still refer to the same material.

## Rules

- **Change the modules, not the story.** If the outcome itself changed, that's a new
  manifest, not a refresh.
- **Only touch what the change affects.** Resist rewriting everything; that's how you
  introduce regressions and burn time.
- **Always re-verify what you touched.** The product is the source of truth, and it just
  moved.
- **Do not invent observation.** Missing submissions mean unknown. Demo records and
  manually marked completion are not runtime evidence. Never claim access to private
  agent chats, local files or terminal history that learners did not submit.
- **Keep the scope small.** A learner's report is a signal to investigate; reproduce the
  issue before treating it as a product defect or rewriting the lesson.

## Why this matters

This is where the workspace stops being a one-time output and becomes an asset you maintain.
A product that ships weekly would otherwise leave your enablement content wrong within a
month; the refresh loop is what keeps a whole library of use cases true over time.
