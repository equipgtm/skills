# Build recipe — a hands-on workshop from the story

A workshop is the deepest enablement artifact: the audience reaches the outcome by doing
it themselves in the chosen exercise environment. Build it from the agreed plan and story,
keeping lesson pages, exercises, code, scripts, notebooks, deck and assets in the same Git
repository. Read [repository.md](repository.md) for the full artifact and release layout.
Use the branded shell when a static site fits the selected content host, or adapt the
pages to the customer's requested format. The instructor uses their own coding agent to
author the files; JSON metadata cannot replace them.

## Plan the artifact before generating pages

For a new substantial workshop, follow [intake.md](intake.md): record a concise plan,
resolve material unknowns with available host capabilities, and preserve supplied choices.
Choose content hosting, execution and feedback independently. The module pages should
point learners to the correct exercise environment without assuming the pages run code.

## Turn the manifest into module files

Preserve an existing host's page layout, frontmatter, navigation, shortcodes and asset
paths. For the bundled standalone renderer, write one `NN-slug.md` file per module in a
content directory, using its header format as shown below. The teaching jobs apply to
other formats too; do not migrate an existing AWS Workshop Studio repository just to
match this example.

````markdown
title: See the drift you can't see today
weight: 1
duration: 20 min
group: Build the checks
summary: Surface mismatched entitlements across services with the catalog MCP.

## Why this step matters
<one short paragraph tying this step to the customer outcome — the customer_value>

## Do it
<numbered, copy-pasteable steps. Every command in a fenced code block.>

!!! output "What you should see"
    ```text
    <the real output — this is the module's `proof`. Paste the actual run, not a guess.>
    ```

!!! exercise "Try it"
    <one short task that makes the learner adapt the step to their own context>
````

Rules that keep it outcome-first and trustworthy:

- **Open every module with the outcome, not the feature.** The first paragraph says why
  this step moves the customer toward the goal. The capability is how, introduced second.
- **Every command is copy-pasteable** in a fenced block (the shell adds a copy button).
- Show each runnable module's observable check and expected result. Include sanitized
  actual output when the check has been run. An `!!! output` block is the standalone
  renderer's convention; use the existing host's equivalent. For content-only preparation,
  label anticipated output and unrun checks explicitly instead of presenting them as proof.
- **One capability per module.** If a module sprawls across three capabilities, split it.
- Include the actual edits needed for an exercise, its starting state, expected result
  and a reset/recovery path. A command that only runs tests does not explain how to make
  the change being taught.
- Label checkpoints so a learner can explicitly submit a result against a named module
  and workshop version. The static shell does not collect those results automatically.
- For the standalone renderer, add `_overview.md` with a short hero and the
  `{{MODULE_GRID}}` token where module cards should appear, and `group` values matching
  the brand's `group_order`. Other hosts retain their existing overview/navigation format.

## Verify the requested scope

Hand the plan, repository artifacts and product source to a separate verifier subagent
(`agents/verifier.md`); include an existing manifest when useful. Give it the actual task
scope and available environment. It should review claims and teaching steps, inspect
rendered pages/files, and run the exercise checks that are authorized and possible.
If a separate agent is unavailable, use the same checklist in a distinct review pass
and label it self-review; do not claim an independent check.

Fix demonstrated defects and unsupported claims. Content-only preparation can finish
with source/render checks and explicitly unrun runtime checks; it must not invent
successful output or expand into deployment to claim completion. Keep each check's
`passed`, `failed` or `not-run` result distinct. Record actual outputs and version/date
where available. The renderer itself does not verify product behavior.

## Exercise code, scripts and notebooks

Create the runnable files requested by the workshop, alongside its instructions. Each
exercise needs a known starting state, meaningful learner edits, a reproducible check and
a recovery path. Include complete examples only when they help teach or recover; keep
instructor solutions out of the initial learner path unless intentionally shared.

For a notebook workshop, deliver actual `.ipynb` files with instructional Markdown cells,
setup/import cells, the exercise code, checkpoints and cleanup. Pin dependencies and
provide retrieval instructions for data the notebook needs. Document opening or importing
a learner copy in the chosen provider, including account/project/region requirements.
Validate from a fresh runtime or identify that check as incomplete. Clear credentials and
private saved outputs before sharing. The notebook can be launched from the workshop page
without moving all teaching pages and feedback collection into the notebook provider.

Author preflight, setup, reset and cleanup helpers when useful, scoped to this workshop.
Keep permission/account checks distinct from resource creation. Scripts act in the
learner's or vendor's authorized environment; EquipGTM never supplies vendor accounts or
credits. An optional learner-agent setup prompt should read and explain these files before
helping execute the authorized steps.

## Render the selected site format

Use the existing repository's documented renderer/build for a customer or AWS Workshop
Studio site. Content-only work can produce a validated local preview without publishing.
The following instructions apply when the standalone EquipGTM renderer is selected.

Write a legacy renderer `brand.json` for the company (see
[brand.example.json](../assets/workshop-shell/brand.example.json)):
company name, product title, tagline, a logo glyph, the palette (`accent` drives the
whole theme), optional fonts, `group_order`, and sidebar `links`. Then build:

```bash
python scripts/build_workshop.py <content-dir> --brand brand.json --out site/
```

Here, `python` means the configured Python 3 interpreter with the optional renderer
dependencies installed; see [INSTALL.md](../INSTALL.md). Use full script paths when the
skill and workshop source are in separate folders.

Need a hero image, an architecture diagram, or icons? Generate them with the
available image-generation or diagramming skill and reference the assets in the module
Markdown. The renderer does not copy content assets: copy referenced images and files to
the matching paths under `site/` when packaging, then check the links in the exported site.

You get a Workshop Studio-style static site: persistent left sidebar with collapsible
groups, focus mode, copy buttons on every block, terminal-style output blocks, and
prev/next paging — in the customer's colors and type. Serve it with any static server:

```bash
python -m http.server --directory site 8080
```

## Deliver the workshop

Use [delivery.md](delivery.md) to build a learner release from the recorded repository
commit, keeping pages, code, notebooks, slides and assets consistent. Include
prerequisites, vendor-access instructions, version information and explicit submission
instructions. Add tutor guidance for use in the learner's own agent when appropriate.
Bundle creation and a local preview do not publish the workshop or provision a cohort.

Studio has a separate instructor/learner preview and ZIP export path. Its hosted service can
serve released files and collect submissions; local mode keeps data on that device.
Neither path runs this Python renderer, executes exercises or verifies product claims.
Demo examples remain labeled as demo content.

## Brand the teaching material

Use the supplied company name, logo and palette consistently on the start page, lessons,
requested slides and survey. Preserve logo proportions and test the rendered identity on
its actual backgrounds, including narrow screens and the closing survey. Do not sacrifice
readable text, links or focus states for an exact decorative color match. If no customer
brand is supplied, retain EquipGTM defaults; for this legacy renderer, explicitly set the
company to EquipGTM rather than shipping its `Your Company` placeholder.

Studio's **Branding** tab previews a per-workshop configuration; the agent can also use
`equipgtm_set_branding`. Its canonical `branding` object is documented in
[studio-agent.md](studio-agent.md). The Python renderer does **not** accept that object
directly. When that renderer is the selected content host, map deliberately:

| Studio field | Legacy `brand.json` treatment |
| --- | --- |
| `companyName` | `company` |
| `accentColor` | `colors.accent`; inspect text/link contrast in the resulting site |
| `headerColor` | No equivalent header field; a workshop-scoped shell change is needed to reproduce it |
| `logoDataUrl` | No equivalent image-logo field; `spark` is an escaped text glyph, not image markup |

The legacy renderer also has `product`, `tagline`, `colors.ink/bg/accent2/accent3`,
`fonts`, navigation groups and links. These are renderer-specific settings, not extra
Studio fields. Keep the formats separate, and use the existing host's branding support
when it differs. Do not paste arbitrary CSS, font configuration or external logo URLs into
Studio branding. Retain the original logo in the repository even when the web copy is
resized. Render a supplied vector logo to a supported raster format for upload, preserving
its design and transparency; do not redraw the company's mark. Choose its light or dark
variant to suit the header. Updating a page theme does not modify a previously rendered PPTX; regenerate and
inspect the deck from its source as described in [presentation.md](presentation.md).
