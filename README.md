# EquipGTM skill

Build technical workshops with your own coding agent. Keep lessons, exercises, code,
slides and feedback questions in a workshop repository you can review and version.

The `equipgtm` skill helps developer advocates, partner engineers and customer architects
plan the workshop, ground it in real product documentation, build the material and
check what learners will receive.

## Install

Run this in the repository where you want to build a workshop:

```bash
npx skills add equipgtm/skills --skill equipgtm
```

Select your coding agent when prompted. The CLI defaults to project installation; choose
global installation to use the skill across projects. It requires Node.js 22.20.0 or newer.
Find it on [skills.sh](https://skills.sh/equipgtm/skills/equipgtm).
For a manual install, use the [GitHub release ZIP](https://github.com/equipgtm/skills/releases/latest/download/equipgtm-skill.zip)
and [installation guide](skills/equipgtm/INSTALL.md).

## Start with an outcome

Open a fresh agent session in your workshop repository. Invoke `$equipgtm` in Codex,
`/equipgtm` in Claude Code, or ask your agent to use the EquipGTM skill:

> Build a 60-minute workshop for developers who need to make failed webhook deliveries
> safe to retry. Use the product documentation and starter repository I provide. Plan
> the lessons, runnable exercises, presentation and feedback questions. Learners will run
> the code locally. Keep the source in Git and report which checks you ran.

The skill can help produce:

- Instructional pages, setup steps, exercises, example code and verification scripts.
- Presentations with a teaching story, readable slides and instructor-controlled reveals.
- Learner downloads, agent prompts, instructor notes and facilitation guides.
- Surveys and a revision plan based on feedback learners choose to submit.

It uses the tools available in your agent. An optional Python renderer builds standalone
workshop pages; presentation rendering uses an available deck tool. If a check or renderer
is unavailable, the skill keeps editable source and reports what remains unverified.

## Deliver with EquipGTM Studio

The skill works locally without an EquipGTM account. [EquipGTM Studio](https://equipgtm.com)
adds hosted learner pages, branded workshops, uploaded files, frozen releases and survey
results. Create a workspace when you want to publish there.

A compatible browser client can expose Studio's WebMCP tools to your agent. Installing
the skill alone does not connect your browser or account. You can also import drafts,
upload files and export feedback through the UI. AWS Workshop Studio, a customer site
or another content host can remain your delivery destination.

You or the vendor arrange product accounts, environments and credits. Learners use their
own tools; EquipGTM does not supply cloud accounts or coding-agent subscriptions.

## Source and feedback

Read the [skill](skills/equipgtm/SKILL.md), its [Studio tool reference](skills/equipgtm/references/studio-agent.md)
or the [skills.sh installation docs](https://skills.sh/docs/cli).
Report reproducible skill issues in [GitHub Issues](https://github.com/equipgtm/skills/issues).
Omit credentials, private workshop material and learner responses from public reports.

Run `python scripts/validate.py` from this repository to check the packaged file inventory,
hashes, links and Python helpers. `skill-manifest.json` matches the downloadable skill
package; the public website's app and infrastructure are maintained separately.

The skill and its included helpers are licensed under [MIT](LICENSE).
