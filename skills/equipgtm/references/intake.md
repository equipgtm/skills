# Intake and plan — make the workshop buildable

For a new workshop or substantial curriculum redesign, plan the teaching outcome and
repository before generating the full set of artifacts. A small correction to an existing
workshop can use a short targeted plan. Start from the user's supplied answers and current
repository; never repeat a question whose answer is already available.

## Read before asking

Read the request, existing files and linked product sources. Identify the audience,
outcome, current workaround, requested duration, artifacts and constraints. Use the
actual SDK, documentation, sample or sandbox to ground what can be taught. A marketing
page supplies context; seek a buildable source before claiming an exercise is runnable.

Propose a concrete customer scenario where the request is vague. A workshop about a
product needs a result the learner can achieve with it. Keep assumptions explicit and
revise them when the user supplies better information.

## Use the host's planning tools when available

Use a host-provided planning capability when it is available and permitted in the current
mode. A skill cannot switch the host into Plan mode, unlock a question tool or override
its execution rules. If the host does not offer those capabilities, save a concise
`PLAN.md` in the workshop repository and communicate the main decisions directly.

Use the host's question tool when it is available and permitted for genuine unresolved
choices. Ask only the questions that materially affect the work; otherwise use a concise
plain-text question. Continue independent research or inspection while answers are
pending. Do not ask for an approval of the whole plan as a ritual, turn every default into
a question, or repeat permissions already granted. A supplied plan or clear brief can be
recorded and used immediately.

## Decisions to capture

| Decision | What to settle |
| --- | --- |
| Outcome and audience | What learners can do afterward, their roles and technical depth, and the customer scenario |
| Teaching format | Duration, live/self-paced, hands-on versus watch-along, module arc, demo and Q&A time |
| Source repository | Existing/new local Git repo, requested remote host/owner, source conventions and requested files |
| Content host | Where the pages, module instructions and material links will be delivered |
| Exercise environment | Where the actual work runs: local code, notebook, vendor console or provided sandbox |
| Feedback destination | Which form/store receives surveys and explicit checkpoint submissions, and who owns it |
| Access responsibility | Who supplies accounts, licenses, projects, credits and vendor permissions; what is already available |
| Setup and recovery | Prerequisites, preflight, resource setup, reset/cleanup, support contact and fallback |
| Agent guidance | Whether an optional learner setup/tutor prompt helps, and which agent the learner already has |
| Artifacts | Required pages, exercises, example code/scripts, notebooks, PPTX/source and supporting assets |
| Customer brand | Supplied guide/logo, company display name and colors; otherwise EquipGTM defaults |
| Verification and release | Runnable product source, planned checks, evidence location and how a cohort gets a frozen version |

**Content host, exercise environment and feedback destination are independent choices.**
An instructor can keep source in GitHub, serve pages on a customer site, run exercises in
Colab and collect feedback in the customer's form tool. A notebook is one artifact and
execution surface; it does not replace the rest of the workshop repository. See
[repository.md](repository.md) for the layout and delivery boundaries.

EquipGTM never owns vendor account provisioning. Record the named party responsible and
author setup instructions or scripts for actions in their authorized environment. A
local UI setting, account sign-up link or exported script is not evidence that accounts,
credits, cloud resources or a feedback service have been provisioned.

Reuse the customer's supplied guide and logo rather than asking for them again or
inventing a replacement mark. Resolve material gaps early, such as which of two supplied
logos to use or a missing display name for requested white labeling. A missing brand is
not a blocker: retain EquipGTM defaults while building the artifacts. Keep original assets
and their source in the repository; derive the supported web logo and slide assets from
them. The plan should say whether branding is supplied, defaulted or still pending.

Apply the chosen identity across workshop pages, the requested deck and feedback form.
Studio branding is per workshop, not custom-domain setup, enterprise identity or an
external form integration. Existing third-party hosts/forms use their own supported
branding controls; record any visual limit instead of promising automatic propagation.

## The saved plan

Keep `PLAN.md` short enough to review. Record:

- Audience, outcome, scenario and the product source to verify against.
- The module journey and rough timing, with an observable check per meaningful step.
- The three destinations, repository owner/location and access responsibilities.
- Files to create or revise, setup/preflight/cleanup needs and optional learner-agent prompt.
- Selected brand and source assets, including any pending customer styling decisions.
- Verification approach, intended release handoff, assumptions and remaining blockers.

Then build the requested repository files and maintain optional machine-readable metadata
where the tools need it. The agent handles any JSON behind the scenes. The presenter
shares a workshop URL; learners open the instructional pages and download the relevant
code/prompts/skills to begin. The complete Git repository and the releases built from it
remain the deliverables, rather than a manual JSON workflow. Reuse an agreed outcome and scope;
only unresolved decisions that block a dependent step need to pause that step.

## Handling an incomplete brief

Choose useful defaults for reversible authoring decisions. Dates, public URLs and a
remote Git host can remain pending while you author locally. Do not invent a working
URL, a deployed environment or a verified output to fill a field.

If the product source is missing, find an official quickstart or sample when available.
If no runnable sample exists, propose a small teaching example or a narrated demonstration
and state what still needs verification. Avoid promising hands-on behavior that has not
been reproduced.

For example, an FDE asking for an ADK workshop in Colab has specified the execution
surface, not necessarily the page host, repository host, feedback tool or Enterprise
app entitlement. Read the current official example, propose a concrete agent outcome,
record the notebook in the repository plan, and ask only about those unresolved delivery
or access choices that affect the requested work. Do not replace their notebook choice
with a local-agent-only workflow.
