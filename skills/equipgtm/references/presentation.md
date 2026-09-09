# Workshop presentations

Use this recipe when a workshop needs slides, a technical introduction, a teaching
storyboard, or a revised deck. The preferences here are adapted from the user's
**Tech Presentations** skill (its story, copy, reveals and QA guidance). They are bundled
in EquipGTM so the authoring agent does not need that separate skill installed.

A workshop deck helps an instructor move a room from understanding a problem to trying
and checking a solution. It accompanies the lessons; it does not put the entire lab on
screen. Preserve useful content and navigation when revising an existing deck. Review-only
requests call for findings, not edits.

## Plan the learning arc

Read the delivery brief from [intake.md](intake.md): event setting, presenter and customer
organizations, speaker roles, audience size/depth, outcome, module order, proofs, access
plan and allotted time. Resolve material uncertainty using its early direction check;
reuse an accepted brief rather than asking again. Put the story in a storyboard before
rendering, then inspect a representative sample before building the full deck. One
communication job per slide is the unit of design. For a live instructor workshop,
produce editable PowerPoint and source unless another format was requested; a PDF is
a review/export companion, not a substitute for the presentation.

Use the following beats where they serve the workshop, combining short beats when useful:

1. **Welcome and context.** Identify the workshop, host/presenting organization and
   speakers with their roles. Explain why this customer audience is here and what the
   session promises. Use the actual event details; pending names stay pending in drafts.
2. **Problem and payoff.** Start with a concrete situation this audience recognizes.
   Show the result they will build or inspect before naming the services underneath it.
   Describe the promised result as the workshop goal until it has actually been verified.
   For an application workshop, show the actual UI or a runnable demonstration of the
   intended user journey. Name its input, action and output in language a customer uses.
3. **The route through the session.** Show the meaningful steps, which parts are
   explanation versus hands-on, the checkpoints and the time reserved for questions.
   Use the actual module titles; a list of vendor names is not an agenda. Include relevant
   breaks, support arrangements and speaker handoffs in the run of show and notes.
4. **The whole application.** Before the first lab, show a complete architecture with
   named components, their roles, boundaries and the path of a request and its data.
   For a published blueprint, map its parts to the workshop and explain substitutions.
   Distinguish runtime flows from tracing and offline evaluation; do not connect every
   tool as though it were another sequential request step. Follow the overview with
   focused component explanations. Reveal the diagram at the presenter's pace.
5. **Join and get ready.** Once the audience understands what they will build, show an
   easy-to-type workshop URL, what to open, the access owner and where to ask for help.
   No workshop QR code. Put detailed installs and credit instructions in prerequisites.
   Pre-event access links may be shared earlier; they do not replace this orientation.
6. **Concept before mechanics.** Introduce a new idea with a worked example: the input,
   the behavior that matters, and its result. Name the concept once the example gives the
   term meaning. For a technical audience that already knows it, go directly to the
   relevant design choice. Do not invent tautological definitions to fill a slide.
7. **Explain → demonstrate → try → check.** For each module, connect a visual explanation
   to a small demonstration, then give learners one action and a visible success check.
   Keep complete commands and recovery paths in the lesson. Include a regroup cue so
   the instructor can resume the room without skipping people who need help.
8. **Connect the pieces again.** Return to the overview and trace one actual request or artifact through the architecture,
   showing boundaries, dependencies and why the important components are there. Explain
   product decisions through their role in the outcome, not a feature catalogue.
9. **Recap, transfer and questions.** Return to the opening problem and the results the
   audience should now be able to reproduce. Separate verified evidence from expected
   outputs. Name a useful next application, leave the promised Q&A time, and close with
   the survey link and, when available, its QR code.

Allocate explanation, demos, hands-on work, transitions, setup recovery and Q&A within the
session length. Write timing in notes rather than cramming it onto every slide. Preserve
section cues at real subject changes. The closing survey can stay on screen during Q&A.
This is coverage for a live technical workshop, not a fixed slide count for every format.
Do not force an unrelated template scenario onto the user's blueprint or customer outcome.

## Words, notes and visuals

- Default to **40 words or fewer per slide**, counting the title, labels, captions, URL
  text and all content across reveal states. Animation does not create a second word
  budget. Follow a user's stricter limit. Record deliberate exceptions for necessary code,
  tables, quotations or references with a reason; do not shrink type to evade the limit.
- Give each title a useful job: a concrete label, real question or supported claim. Read
  it with the talk track. Cut repeated ideas, empty promises, slogan fragments and wording
  the instructor would not say. Use `no-ai-slop` for the final copy pass when installed; otherwise perform the same
  plain-language review directly from these criteria. A word blacklist cannot approve the meaning of a slide.
- Name the concrete user task, tools and behavior. A phrase such as "a policy question
  with missing evidence" needs the actual question and missing source explained; it is
  not sufficient workshop context. Use the verified scenario's own terms, not an invented
  replacement story. Keep necessary technical terms, agenda and section labels. Do not
  compress away meaning to meet the word budget: split the explanation across slides.
- Put the explanation in speaker notes: what to say, what to point at, why the step
  matters, the click sequence, demo/hands-on instructions, expected output, recovery cue,
  time allowance and handoff to the next slide. Keep instructor answers out of learner
  copies unless their teaching format calls for them.
- Use the customer's brand and a varied sequence of flat layouts. Start near 50 pt for
  deck titles, 35 pt for slide titles, 24 pt body and 18 pt chart labels; adjust for the
  room and rendering. Crowding calls for editing or another slide, not smaller type.
- Use **diagrams for relationships**, charts for patterns, small tables for precise
  comparisons and lists for parallel reasons or steps. An architecture slide needs a
  visible path through the actual application, not a paragraph or anonymous boxes.
- Use icons to identify meaningful actors or actions: learner, application, worker,
  database, request, result. Keep the same icon and label for the same concept. Pair an
  unfamiliar icon with a short label and group them for reveals. Use genuine vendor
  marks where appropriate. Decorative icons on every bullet add no explanation.
- Use real screenshots, logs, code or charts when they establish a factual claim. A
  generated picture can explain a concept but cannot prove behavior. Show only the code
  lines or crop the audience needs, usually no more than 12 lines; keep full detail in
  the lab. Inspect every asset at full size for legibility, crop and distortion.
  When the application is not running yet, mark the screenshot/demo as pending in the
  storyboard, then capture the real application after it runs. An explicitly labeled
  wireframe may support early planning; never pass it off as a product screenshot.
- Give slides unique semantic titles, meaningful alt text and sensible reading order.
  Use sufficient contrast and avoid relying on color alone. Notes should contain complete
  `[Sources]` / `[/Sources]` blocks for external claims and assets; use `Presenter
  synthesis` when there is no external claim, and identify actual verification evidence
  separately from planned proofs.

## Reveal the explanation at the instructor's pace

For a process, diagram, comparison or code walkthrough with several spoken beats, plan
what the audience sees **before the first click**. Add native PowerPoint entrance effects
that the instructor advances manually. Appear, Fade or Wipe are usually enough. Reveal
one useful unit of explanation, with its label and connecting arrow, rather than words
or decoration. Leave earlier material visible when it is needed for context.

Record the sequence in notes, for example:

> Start: learner and request. Click 1: application receives the request. Click 2:
> worker processes it. Click 3: result returns to the learner. Keep earlier steps visible.

Do not place a completed diagram behind animated overlays. Avoid automatic delays or
movement that distracts from the explanation. A one-message slide may stay static.
A transition between slides, an empty timing tree or a storyboard click list does not
implement object reveals in a PPTX.

Use an available presentation renderer that can implement native effects, or valid PPTX
timing supported by the available tools. If native effects remain unavailable, progressive
duplicate slides with stable positions and manual advance are a portability fallback.
Identify the fallback in the delivery notes; do not silently substitute it for requested
native animations. The browser storyboard preview is a planning aid, not PowerPoint
playback or a generated deck.

## Carry the customer brand into the deck

Read the selected workshop branding and supplied brand guide before rendering. Reuse the
same company name, original logo and palette as the instructional pages and survey.
Preserve logo proportions and clear space, and use a supplied variant that remains
visible against the chosen background. Do not invent a customer mark or treat a product
icon as the customer's identity. With no customer brand supplied, use EquipGTM defaults.
Separate the host/customer identity from the products being taught. Obtain real product
logos from supplied or official assets, record their sources and preserve their shapes.
Do not substitute typed initials, invented marks or generic icons for requested logos.
If an asset is unavailable, use a plain product label and report the missing logo.

Keep editable slide source and original brand assets in the repository. Studio branding
styles its workshop pages and survey, but it does not recolor, replace logos in or
regenerate an uploaded PPTX. Apply changes to the source, rerender the actual deck, inspect
it and attach the resulting version before saving the next release. An external survey
needs its own supported styling; Studio cannot restyle another provider's form.

Check the actual company name, logo crop, text/background contrast and readability at
presentation size. Branding must leave room for the teaching content: visible wordmarks,
footers and labels still count toward the 40-word limit. The workshop join remains a
typed URL with no QR; only the closing survey may use a QR with a readable URL fallback.

## Workshop and survey destinations

**Workshop join:** display a short, easy-to-type URL for laptop users. Use a real,
verified, team-controlled destination supplied by the instructor or returned by a
connected link service. Prefer a durable session landing page so setup instructions,
material downloads and the taught release stay together. Do not add a workshop QR code.

**Survey close:** show the readable survey URL and, when the destination exists, a QR
code encoding that same URL. Keep the readable URL as the fallback. Label its purpose
and allow time to respond. Use adequate contrast, an intact quiet zone and enough size
for the room; test a scan of the actual projected/exported slide. Link the survey to the
session/release being taught so draft edits cannot change the old questions.

Keep these links in one session delivery record and bind them when preparing that
session's deck. Reuse the curriculum/storyboard for a new cohort, but resolve that cohort's
links again. A learner URL should not point to an instructor route or include credentials.
A future short-code service should resolve an opaque code to the authorized session and
release (and enrollment where needed), rather than accept arbitrary redirect targets.
Keep authentication tokens and expiring signed ZIP URLs out of slides and QR codes.
Use a stable landing page instead. The download action behind the page can obtain a fresh authorized signed URL.

Local mode has no shared survey hosting. The hosted service serves session pages and feedback,
but does not create branded short URLs. An entered URL or local preview is not evidence
that a destination has been created or published. If no
working URL exists, retain an explicit `Workshop link pending` or `Survey link pending`
placeholder in the draft and list it as unfinished. Do not manufacture an active-looking
short URL or QR code for a placeholder. Localhost links are only suitable for a local
preview; they do not work on the audience's laptops or phones.

## Author, render and verify

Keep the editable storyboard and notes under `slides/` alongside the workshop's source
manifest, brand and evidence. Start from [../assets/presentation-template.json](../assets/presentation-template.json)
when useful; it is an editable example with pending URLs, not a tested workshop. Follow
the Studio presentation settings in [studio-agent.md](studio-agent.md) when exchanging
canonical curriculum. In the local UI, use **Materials → Presentation** to edit the
storyboard and download its authoring brief. The source
storyboard and rendered PPTX are separate artifacts; neither is implied by an asset badge.

Discover the current agent's available presentation tools when a rendered deck is
requested. Use an installed presentation skill for authoring/rendering mechanics when
available; these EquipGTM rules supply the workshop story, links and quality requirements.
If no renderer is available, retain editable source and identify the unrendered deck.
Do not require the user's separate `tech-presentations` installation.

Run the bundled structural audit with the configured Python interpreter, for example on
this machine:

```bash
python scripts/audit_presentation.py slides/workshop.pptx --require-reveals 4,6-8
```

Use `--max-words 39` for fewer than 40 words, `--allow-over 7,12-13` for recorded exceptions,
and `--json` for a machine-readable report. The audit counts all stored slide text, not
text embedded in screenshots, and checks declared click entrance targets. It cannot prove
initial visibility, reveal order, URL reachability, QR readability, natural copy, good
composition or accessibility. Notes and image-alt coverage are mechanical checks only.

Complete the checks the actual deliverable needs:

0. Before full rendering, review the storyboard as someone arriving at this event:
   can they tell who is teaching, why they are here, what application they will build,
   what it looks like, how its components connect, how the session is organized and
   when to open the workshop? Check each required job against an actual slide and
   evidence asset, not just a promise in notes. For blueprint workshops, confirm all
   intended parts and substitutions are explained. For live delivery, check section
   introductions, practice/regroup cues and a usable run of show. Fix missing context
   before spending time on complete layouts or animations. Record justified omissions
   for other formats. Audit the rendered sample for the same jobs.
1. Render every slide; inspect the montage for the full story and each slide at full
   size for wrapping, clipping, overlap, asset quality and readability. Check final
   reveal states against the word budget. Fix overflow and unclear copy.
2. Verify the workshop URL by typing it and following the learner route. Verify the
   survey URL and decode/scan its QR to the same destination. Confirm the session/release
   and the fallback instructions. No workshop QR should be present.
3. Open the final PPTX in PowerPoint when available. Inspect representative layouts,
   then play the entire deck in Slide Show: first state, each click, transitions, demo
   cues, links and media. Compare each reveal to its notes. Save, close, reopen and replay
   representative sequences. A static render is not evidence of native playback.
4. Run PowerPoint's Accessibility Checker when available and address title, alt-text,
   reading-order, contrast and media issues. Rehearse the required offline/demo fallback.

Deliver the requested artifact with the slide count, maximum word count and exceptions,
render/overflow result, link and survey-QR results, native reveal/playback result and
accessibility result. Report unavailable or unfinished checks plainly. Do not call a
PPTX verified because the audit passes, or claim a storyboard is a completed presentation.
