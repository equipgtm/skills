# Deliver recipe — portable workshops for real cohorts

Build prepares and verifies the teaching material. Deliver makes it usable by a learner
with the documented tools and access, and by an instructor who did not write the lesson.
Maintain the complete workshop Git repository as editable source and assign each delivery
a workshop version and source commit. Pages, exercises, scripts, notebooks, slide source,
PPTX and supporting assets belong to that project; a JSON export is only part of the
handoff. Follow [repository.md](repository.md) for source and archive packaging.

## Separate the delivery destinations

Resolve the content host, exercise environment and feedback destination from the saved
plan, independently. Pages may live on a customer site while exercises run in a notebook
or vendor console and feedback goes to an existing form tool. The source Git host is a
separate choice. Record each destination's owner, learner entry route and any pending
publishing step. Reuse answers already supplied; changing the exercise environment does
not imply moving the pages or survey.

## Start at the workshop URL

The presenter's typed URL should open the instructional start page, where learners find
setup, module navigation and the relevant code/prompts/skills to download. Explain where
to place the files and how to start the first exercise in the chosen environment. Link a
notebook or console directly when that is the intended exercise path. Do not send learners
through a manifest editor or a JSON import screen to use the workshop.

## A learner bundle

Package the material the workshop actually needs:

- `START-HERE.md`: outcome, audience, workshop/product versions, approximate duration,
  supported environment and where to ask for help.
- Lessons: a static site or readable Markdown, with referenced images and files included.
- Exercises: actual starter code, example scripts and requested `.ipynb` notebooks, with
  explicit changes to make, checkpoint commands/results, dependencies and recovery/reset
  instructions. Pin any external repository/data dependency to the tested version.
- Presentations: the requested PPTX and editable source/assets, with an instructor copy
  for private notes/answers. An outline or storyboard does not satisfy a requested deck.
- `PREREQUISITES.md`: installation steps, account/plan requirements, access owner,
  expected usage costs, and cleanup instructions when exercises create resources.
- Submission instructions: the chosen survey and check-result destination, module/check
  identifiers, and what the learner should deliberately submit.
- Metadata: story/release information and optional canonical `workshop.json` for Studio
  interchange. These describe and organize the files; they do not replace the code,
  notebooks, page assets or presentation. Include the survey definition and the chosen
  submission route. Prototype learner exports remove instructor slide notes; review
  separately shared PPTX/PDF files for facilitator-only content.
- Optional `TUTOR.md`, setup prompts and workshop-scoped skills: downloadable guidance
  with clear instructions for the learner's chosen coding agent.

Keep facilitator answers, verification reports and instructor notes in the instructor
workspace unless they are intended for learners. Include an answer key where the teaching
format calls for it. Copy only teaching assets into the bundle; vendor credentials and
private source material are not learner assets.

Open the exported material as a learner would. Check its starting instructions, relative
links, referenced files and version labels. For the Python rendering path, images and
other content files must be copied into the matching output paths separately. Extract the
archive outside the source workspace and test relative links, notebook imports and the
starting instructions. Record its source commit and checksum. A ZIP omits Git history and
captures a release snapshot; retain the source repository for future authoring. Publishing
and sharing the archive are separate operations.

## Rehearse the delivered path

Check the experience the audience receives: **workshop URL → instructional page → download
or launch → setup/preflight → exercise/check → feedback**, using the release and access
plan for that cohort. The Python renderer does not copy referenced code, notebooks,
prompts, skills or images; package them into the matching published paths explicitly.
Test actual downloadable files after extraction and use a fresh learner starting state
for the runnable steps. When authorized and applicable, verify the feedback route with a
clearly labeled test submission, then exclude that record from real results.

Check the actual published URL when a host has been connected and publishing is in scope.
Otherwise verify the local preview/archive and report public URL or remote feedback checks
as pending. A same-browser local prototype does not prove that a participant on another
computer can reach the workshop or submit shared results.

## Vendor access and prerequisites

Choose an access plan for the workshop:

| Plan | Learner setup | Owner |
| --- | --- | --- |
| Learner-owned | Learner signs in to the required product/agent with their own account | Learner |
| Provided sandbox | Instructor or vendor provisions a dedicated training environment | Named instructor/vendor contact |
| Watch-along | Instructor demonstrates the steps; learners receive material and exercises for later | Instructor |

Record product names, versions, account requirements and any plan limits that affect the
lesson. Explain what learners can complete if access is unavailable. EquipGTM Studio
organizes the plan and material. EquipGTM never owns vendor account provisioning, bundles
or resells third-party coding-agent subscriptions, issues vendor credentials or promises
credits. The learner or named instructor/vendor supplies access. Workshop scripts may
guide or perform authorized setup in that party's selected environment; exporting a
script does not mean it has run.

Document prerequisite checks separately from resource creation. Preflight should identify
the selected account/project/environment and check the relevant runtime, dependencies and
permissions without making unrelated changes. Scope setup and cleanup to workshop-owned
resources, document expected costs and preserve a reset/fallback path. Do not treat unknown
access or unexecuted checks as ready.

## Optional tutor instructions

Use a short `TUTOR.md` when learners would benefit from guided help in their own agent.
When setup is the main friction, also provide a paste-ready `AGENT-START.md` prompt that
asks the learner's agent to read prerequisites, inspect setup scripts, explain logins and
work within the selected environment. Keep credentials out of the prompt. Learners do
not need an agent subscription when the workshop can be completed directly in its
notebook or console.

Include the outcome, workshop version, module order, environment, useful hint sequence,
where to find expected results and when to ask the instructor. Ground guidance in the
delivered lessons. Let the tutor help the learner reason through a task without claiming
to see files or execution results it has not been given.

Tutor output is advice, not proof of completion. The learner chooses which checkpoint
result or excerpt to submit through the documented channel. EquipGTM Studio does not
read their agent session automatically.

## Cohorts and versions

A cohort record associates a group with a specific workshop version, instructor, delivery
mode, optional schedule, support route and submission destination. It is not an invitation
or evidence that anyone attended. Record invitations, attendance and submitted results only
when those actions actually occurred and the information is available.

Keep a delivered version stable while a cohort uses it. Record the full Git commit for
the curriculum, code, notebooks, slide source and rendered release. Working branch names
can move; check external links use the tested revision. Bind each delivery archive to that
commit rather than claiming a source branch is frozen. Author corrections as a new
version; note which previous version and feedback led to the change. A live correction
can be communicated within the authorized delivery scope, with its version recorded.

Freeze the survey definition with the curriculum. Sessions use the saved release's
questions, choices and scales even when the next working draft changes. Freeze the
presentation settings with the release too; bind the session's actual delivery links when
preparing its deck. Keep response records tied to the session/release and stable question IDs; see [survey.md](survey.md).

## Optional authoring-manifest metadata

The existing `use_case`, `audience`, `outcome`, `starting_point`, `product_source`,
`artifacts` and `modules` fields keep their meaning. The following fields are optional;
an older manifest that omits them is still valid. Missing metadata means unspecified,
never automatically verified or delivered.

| Field | Shape and meaning |
| --- | --- |
| `version` | String such as `"1.0"`; the workshop material's version |
| `planning` | Object with `path`, usually `PLAN.md`; the saved teaching/repository plan |
| `repository` | Object with local `path` and nullable `remote_url`; records actual source location, not an instruction to publish |
| `verification` | Object with `product_version`, nullable `verified_at`, and `evidence_path`; points to actual verifier records |
| `delivery` | Object with `mode` (`live` or `self-paced`), `bundle_path`, nullable `cohort_id`/`starts_at`/`source_commit`/`release_tag`, `instructor`, `support_contact` and optional independent destination objects below |
| `access` | Object with `mode` (`learner-owned`, `provided-sandbox`, or `watch-along`), `prerequisites` as strings and `vendor_accounts` as account-requirement objects |
| `presentation` | Object with `storyboard_path`, nullable `deck_path` and `qa_path`; pointers to editable slide source, rendered deck and actual QA records |
| `tutor` | Object with `enabled`, nullable `instructions_path`/`setup_prompt_path`, and workshop-scoped `guidance` |

Optional `delivery.content_host` and `delivery.feedback_destination` objects use nullable
`kind`, `url` and `owner`. `delivery.exercise_environment` uses nullable `kind`, `launch_url`,
`owner`, `setup_path`, `preflight_path` and `cleanup_path`. Kinds are descriptive labels
for the selected provider or format, not claims of a working integration. Null means
undecided or not yet applicable; record real URLs and source commits only when available.
These authoring-manifest fields are separate from Studio's canonical schema.

An optional `vendor_accounts` entry can use `vendor`, `requirement`, `provided_by` and
`setup_url`. It describes how to obtain access, not an account secret. Dates use ISO 8601.
These fields support authoring and handoff; the existing Python renderer reads module
Markdown and branding, not manifest metadata, and does not enforce any of these states.

Studio uses a canonical `workshop.json` export with `title`, `outcome`,
`audience`, `version`, `modules` (`title`, duration in minutes, `content`), `accessMode`
and `prerequisites`, plus customizable `survey` and `presentation` definitions. These are
optional in older imports; Studio resolves authoring defaults for files that omit them.
Preserve the full authoring manifest and verification evidence separately; canonical UI JSON is not a lossless
replacement for that source workspace.

Use [studio-agent.md](studio-agent.md) for available browser tools or file handoff. Tool
exports in local mode return text and attachment bytes; cloud mode returns a temporary
signed ZIP download. UI exports download a ZIP. Consult that reference for current file capabilities;
do not infer Git synchronization or support for an arbitrary-size repository from local
file attachment support. If an integration uses canonical JSON, the agent round-trips it
and verifies intended fields. This machine interchange remains separate from the learner's
workshop URL, instructional pages and downloads.

For live delivery, follow [presentation.md](presentation.md): use an easy-to-type workshop
URL with no QR at the start, then a survey URL and optional QR at the end. Resolve the
right cohort and released survey before rendering. Keep URLs stable at the landing-page
level; generate authorized short-lived ZIP downloads behind that page, not inside slides.
A reusable source may store default URLs, but each delivery copy must be checked against
its actual cohort. Use the deployed session's verified URL or the instructor's known working
destination; Studio creates no branded short URLs. Pending links stay explicit in drafts;
they must not become fabricated QR codes.

## Local demo and hosted delivery

In local mode, `web/` keeps demo records in browser localStorage and offers previews, surveys,
import and ZIP export. Those records do not constitute shared delivery. The hosted service
uses private file storage, the customer's account for authoring, frozen
release bundles and public session pages with separate participant cookies. It supports
actual file downloads and submitted survey responses. Neither mode provisions vendor
accounts, runs learner agents or proves exercises have executed.

Instructors can also use the source repository and portable files with their existing
hosting/form workflow. Keep expected outputs, learner reports and independently reproduced
evidence distinct, regardless of storage mode.

See [INSTALL.md](../INSTALL.md) for customer sign-in, agent setup and the ordinary UI
fallback. A public session link is not enterprise
enrollment or team membership. A temporary download URL is not the workshop's delivery URL.
