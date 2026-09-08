# The workshop repository

The complete deliverable is a workshop Git repository: pages, modules, exercises, working
code, example scripts, notebooks, presentation source and PPTX, diagrams and supporting
assets, all maintained as one versioned project. Create the files the requested workshop
needs. A manifest describes that project; it cannot stand in for the project itself.

Use an existing repository and its conventions when supplied. Otherwise create a local
workshop repository within the requested workspace. Initializing local Git is distinct
from creating or publishing a remote repository. Do not claim a remote exists until it
has been created through an available tool within the user's scope.

## A practical layout

This layout is a starting point, not a requirement to create empty folders:

```text
customer-workshop/
├── README.md                    # outcome, start here, supported paths and versions
├── PLAN.md                      # teaching arc, deliverables, decisions and open questions
├── manifest.json                # optional machine-readable story and proof references
├── workshop.json                # optional machine-readable Studio interchange
├── brand.json                   # optional legacy static-renderer settings; not Studio branding
├── .gitignore                   # local state, credentials, caches and generated work files
├── .env.example                 # names and harmless examples only
├── workshop/
│   ├── content/                 # overview, setup, numbered lesson pages and module links
│   └── site/                    # optional generated page output for the selected host
├── exercises/
│   ├── 01-first-task/           # starter code, task README and observable checks
│   └── 02-next-task/
├── examples/                    # complete examples when they support the lesson
├── notebooks/                   # .ipynb lessons plus their data/dependency requirements
├── scripts/                     # setup, preflight, reset, verification and cleanup helpers
├── learner-tools/               # optional prompts and workshop-scoped agent skills
├── assets/                      # diagrams, screenshots, icons, original logo/guide and source notes
├── slides/
│   ├── presentation.json        # editable storyboard/settings, when used
│   ├── source/                  # renderer source, notes and layout assets
│   └── workshop.pptx            # generated and inspected presentation, when requested
├── instructor/                  # facilitation guide, solutions and demo fallback
├── survey/                      # question source, external form mapping and export recipe
├── delivery/                    # cohort instructions, target links and release file lists
└── verification/                # sanitized actual results, version and date
```

Follow existing package/dependency conventions. Preserve lockfiles or pinned versions
needed to reproduce a lab. Keep data small and redistributable; document retrieval and
access for large or private data rather than copying it into a public repository. Native
PPTX and `.ipynb` files are actual deliverables, not placeholders satisfied by their JSON
metadata. Record any artifact that remains unrendered or unverified.

Keep the supplied logo and brand guide as authoring source, with enough provenance to
identify the intended company and variant. Studio's optional `workshop.json.branding`
contains its supported name, colors and small embedded logo; it does not replace original
artwork or a slide theme. The legacy renderer's `brand.json` uses a different schema; see
the mapping in [workshop.md](workshop.md). Do not copy a private brand guide into a learner
package merely because its approved logo is visible there.

## The learner entry point

The presenter shares one workshop URL. It opens a readable start page with the outcome,
prerequisites, module navigation and a clear way to download the needed code, prompts or
workshop-scoped agent skills. Each module links to its actual exercise files or external
notebook/console entry point. Tell learners where to put downloaded files and what to do
next. They should not have to interpret a manifest or import JSON to begin.

Keep machine-readable metadata behind this experience. The authoring agent may use it to
maintain Studio records or render pages, but the requested deliverable is the working
repository and its published instructional experience. A local prototype URL is a preview;
report a public workshop URL only after the chosen host is actually published and checked.

## Three destinations, chosen independently

| Decision | What it controls | Examples |
| --- | --- | --- |
| Content host | Where learners read instructions and find materials | Customer site, GitHub Pages, LMS, static files, an existing workshop portal |
| Exercise environment | Where learners edit/run code or operate the product | Local checkout, Colab notebook, customer cloud project, vendor console/sandbox |
| Feedback destination | Where the instructor receives deliberately submitted answers/results | Customer form tool, an existing form endpoint, an authorized workshop service |

The Git host is another source-management choice; it need not serve the pages or execute
the exercises. For example, source can live in the customer's GitHub organization, pages
on their site, a notebook in Colab, and feedback in their form tool. Changing one should
not require replacing the curriculum. Do not infer that choosing a notebook moves the
pages, surveys, credentials or agent hosting into the notebook provider.

Record known destinations and ownership in the plan. An unset destination is a pending
decision, not permission to deploy. Local preview links and UI records are not public
hosting or shared submission collection.

## Scripts and learner setup

Keep setup understandable and reproducible. The prerequisite page should state the
supported runtime, dependency versions, account/project requirements, access owner, cost
or credit arrangement when known, and a watch-along or offline fallback.

Author setup, preflight, reset and cleanup scripts only when the workshop benefits from
them. They can guide or perform authorized resource setup in the learner's or vendor's
selected environment. EquipGTM does not own vendor account provisioning, issue identities,
resell subscriptions or promise credits. The learner, instructor or named vendor contact
supplies that access and approves its environment-specific actions.

Preflight should check the prerequisites that can be checked without changing resources:
selected project/account/region, dependency versions, required API access and a small
scoped connectivity check when suitable. Mark an unperformed check unknown. Keep resource
creation in a separate, explicit setup step. Cleanup should target the resources created
by this workshop, using recorded IDs or a workshop-specific namespace. Avoid commands
that delete an existing shared project, workspace or unrelated data.

An optional `TUTOR.md`, `AGENT-START.md` or `learner-tools/` package can give learners a
paste-ready setup prompt and workshop-scoped skills. Include installation/use instructions
for the agent they actually use; do not assume every host has the same skill directory.
The prompt should ask the agent to read the start page and prerequisites, identify the
chosen environment, inspect the provided scripts, explain any required logins, then help through the named modules and
checks. Tell the agent to work from files/results the learner actually supplies. Keep
credentials out of the prompt. A coding agent is optional for a notebook or console
workshop unless using one is part of the learning objective.

## Keep the repository safe to share

Create a `.gitignore` suited to the stack before adding generated or local files. Exclude
real `.env` files, credentials and OAuth tokens, private configuration, virtual
environments, dependency caches, notebook checkpoints, local build caches and temporary
archives. Keep `.env.example` limited to variable names and non-secret sample values.
Do not exclude the requested teaching source or rendered deliverables by accident.

Review notebook saved outputs and metadata, screenshots, notes and logs for credentials
or private customer data. Clear or sanitize outputs intended for learners. Prefer
sanitized verification evidence and aggregated feedback in the repository; raw learner
responses belong in the authorized feedback store. `.gitignore` does not remove a secret
already tracked by Git or exposed in history.

## Source, releases and downloads

The working branch is the editable source. A delivery uses a recorded commit, with a
release label/tag for navigation. A branch name can move, and a tag alone is not proof
of immutability; record the full commit identifier and the hashes of delivered archives.
If the source is still uncommitted or Git is unavailable, label the handoff as a draft
snapshot rather than inventing a commit or release.

Build a learner ZIP/site and instructor pack from the same frozen source. Use an explicit
file list so the learner package contains the needed lessons, exercises, code, notebooks
and assets while instructor solutions/private notes stay in the instructor pack unless
intentionally shared. Check relative links and notebook imports after extraction, outside
the source workspace. Link external example repositories to the tested commit/release.

Branding belongs to the same frozen version as the teaching material. Studio releases
copy the selected branding; a later draft edit or reset does not restyle existing sessions.
For a branded workshop, Studio bundles include `branding.json`, derived `branding.css`
and, when supplied, `branding/logo.png`, `.jpg` or `.webp` in both learner and instructor
exports. These files are not a full slide theme or a copy of the original guide. Rerender
and reattach an affected deck before freezing its next release; check the actual delivered
pages, survey and PPTX rather than only the working draft's preview.

When using the bundled Python page renderer, copy every referenced code file, notebook,
prompt, skill directory and image into the intended published paths separately. The
renderer does not copy those files automatically. Verify downloads from the generated
site, not only links within the source checkout.

A source repository and a ZIP are different handoffs: the repository supports continued
authoring; the archive is a portable delivery snapshot and usually omits `.git` history.
Rendered pages can be generated by the selected host's build, and large deck binaries
can be attached to the release or managed with the team's established Git LFS policy.
Whichever method is used, retain editable source and record exactly which artifact goes
with which workshop commit. Do not call an outline export the complete repository.

For cohort-specific links, prepare the delivery copy against the frozen workshop and
survey definition. Keep a typed workshop URL with no QR and an end-of-deck survey URL with
an optional QR, following [presentation.md](presentation.md). Stable landing pages can
resolve authorized downloads; expiring signed ZIP URLs do not belong on slides.
