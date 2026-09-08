# Use EquipGTM with your agent

## Install from GitHub

In your workshop repository, run:

```bash
npx skills add equipgtm/skills --skill equipgtm
```

The [skills CLI](https://skills.sh/docs/cli) needs Node.js 22.20.0 or newer. Select your
agent when prompted. Installation defaults to the current project; choose global
installation if you want the skill available across projects. Read the changes before
replacing an existing copy. Start a fresh agent session if skill discovery has not refreshed.

The public source is [equipgtm/skills](https://github.com/equipgtm/skills). The skill and
its included helpers use the MIT license. You can use them locally without an EquipGTM
account; sign in when you want Studio to host learner pages and collect feedback.

If you installed the early `equip` version, install `equipgtm` first and confirm it
appears in your agent. Preserve any local edits, then remove the old `equip` skill from
the same project or personal skill directory so the agent does not discover both names.

## Manual ZIP alternative

Download [equipgtm-skill.zip](https://equipgtm.com/downloads/equipgtm-skill.zip) and extract it. The archive contains one
`equipgtm/` folder. Keep that folder intact: the references, templates and optional scripts
are part of the skill. The accompanying download manifest records each file and its
SHA-256 checksum. This is a portable skill folder, not a marketplace plugin or MCP server.

Move the extracted `equipgtm` folder into the directory for your agent. If an `equipgtm` folder
already exists, compare or back it up before replacing your edits.

| Agent | Personal installation | Project-only alternative |
| --- | --- | --- |
| Codex | `~/.agents/skills/equipgtm/` | `.agents/skills/equipgtm/` in the workshop repository |
| Claude Code | `~/.claude/skills/equipgtm/` | `.claude/skills/equipgtm/` in the workshop repository |
| Cursor | `~/.cursor/skills/equipgtm/` | `.cursor/skills/equipgtm/` in the workshop repository |

The resulting path must end in `equipgtm/SKILL.md`, without an extra nested `equipgtm` folder.
Open the workshop repository in your agent. Select EquipGTM from its skill picker, or
ask it to read the installed `equipgtm/SKILL.md`. Codex CLI/IDE can invoke `$equipgtm`; Claude
Code can invoke `/equipgtm`. If discovery has not refreshed, start a new agent session.

These are local-agent instructions. A remote or cloud agent needs the skill in its own
workspace or that product's supported sync/install flow; local files and browser sessions
are not automatically shared. Other agents can use the extracted folder when they support
Agent Skills or can read its Markdown and supporting files.

Installation locations were checked against the official
[Codex skills guide](https://developers.openai.com/codex/skills),
[Claude Code skills guide](https://code.claude.com/docs/en/skills), and
[Cursor skills guide](https://cursor.com/docs/skills) on 2026-09-08.

## Start a workshop

Sign in to EquipGTM and open **Build with your agent**, the default workspace page.
Copy its prompt into Codex, Claude Code, Cursor or your preferred agent. It invokes this
skill and starts the intake: customer outcome, audience, use cases, technologies and
their roles, access plan, duration and branding. No workshop form is required first.
Use `$equipgtm` in Codex, `/equipgtm` in Claude Code, or select/read the skill in other agents.
For example:

> Use the EquipGTM skill to build a 90-minute workshop for customer developers. Start
> from this repository and the product documentation I supplied. Reuse my brand assets.
> Plan the lessons, exercises, presentation and feedback before generating the artifacts.
> Ask only about missing choices that affect the work. Keep content hosting, exercise
> access and feedback separate. Prepare the workshop repository and the files Studio
> needs. Report checks you actually ran and anything still unverified.

Your agent works in your repository with your existing tools. EquipGTM does not provide
an agent subscription or vendor exercise accounts. You or the vendor arrange any needed
accounts, projects and credits. An agent is optional for learners unless the lesson needs it.

## Connect to Studio when supported

An installed skill gives your agent instructions. It does not connect the agent to your
account. Open the signed-in Studio page in a browser client that exposes WebMCP page tools
to your agent. In **Build with your agent**, a ready status means the page registered its browser
tools; it does not prove your agent can call them.

Ask the agent to discover tools and call `equipgtm_list_workshops` first. Check the
returned workspace and workshop list, then call `equipgtm_get_workshop` for the intended
draft before changing it. Use returned IDs and the current `updatedAt` token. Never copy
cookies, passwords or login codes into prompts. Native Codex, Claude Code and Cursor
connection support depends on their actual browser/client capabilities; this package
does not claim that every installation has a working WebMCP connection.

## CLI fallback

If browser tools are unavailable, open **Build with your agent → Through the CLI**
and create temporary access. Run this command yourself in a terminal, using your actual
installed skill folder and the workspace ID shown in Studio:

```bash
node <skill-folder>/scripts/equipgtm.mjs login --workspace WORKSPACE_ID
```

Paste the access token into the hidden terminal prompt. Never paste it in agent chat.
The CLI stores it in `~/.config/equipgtm/access.json` with owner-only permissions, outside
the workshop repo. An agent running in that same environment can now use the CLI:

```bash
node <skill-folder>/scripts/equipgtm.mjs request GET /state
```

Access is limited to this workspace's workshops, sessions and results, with your current
role. It lasts at most one hour and ends when the originating website session signs out.
Creating new access replaces the previous grant for this workspace. Use **Revoke this
access** in Studio to end it early, or `logout` in the CLI to remove the local copy.
Other machines and cloud agents need their own user-configured connection; do not copy
credentials into workshop artifacts. The API/CLI does not manage invitations or SSO.
Read [references/studio-agent.md](references/studio-agent.md) for payloads and uploads.

## File fallback

If neither browser tools nor CLI access is available, keep building locally:


1. Have the agent author the repository and generate its supported `workshop.json` draft.
2. In Workshops, use **Import draft**, then upload the actual code, notebooks, slides and other
   materials in **Files**. Choose the learner or instructor audience for each file.
3. Review the lessons, branding, survey and rendered materials. Save a release and create
   a session. Open the returned learner link and check its instructions and downloads.
4. Read submitted feedback in Improve. Export the results or give the agent the relevant
   results for revision. Export instructor materials when it needs the latest draft.

The agent handles JSON behind the scenes; a JSON import does not include unattached
repository files or render a PPTX. Browser automation may use these same controls where
your client supports it. The public customer workflow needs your website account, not
the service operator's AWS credentials or its internal pilot bridge.

## Optional script dependencies

Reading the skill and authoring files requires no Python or Node package installation.
The included PPTX audit uses Python 3.10+ and the standard library. It checks structure;
it neither renders slides nor proves native PowerPoint playback.

The optional static-page renderer needs Python 3.10+, Python-Markdown and Pygments from
`requirements.txt`. Ask your agent to use your configured Python interpreter and a local
virtual environment, then install that file with the environment's `python -m pip install
-r requirements.txt`. Run scripts from the extracted skill folder or use their full paths.
Existing customer page builds and available presentation renderers keep their own dependencies.
The static renderer does not copy referenced code, notebooks or images: package them at
the expected paths and test the delivered downloads.

No login configuration, deployment tools, credentials or customer workshop data are
included. Installing the skill does not execute its scripts or publish a workshop.
