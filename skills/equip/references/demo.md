# Demo recipe — the live walkthrough

A demo is the presenter-driven version of the story: you drive, the audience watches the
outcome happen. It's shorter and tighter than a workshop (a few minutes on a call, not an
hour of hands-on), and its whole job is to make the value obvious in one sitting. Build it
from the same manifest — pick the few steps that show the outcome best, and stage
everything so it never wobbles.

## Pick the beats

From the manifest, choose the **2–4 modules** that most directly show the outcome. A demo
is not the whole workshop at speed; it's the highlight reel. The last beat should be the
moment the value becomes undeniable — the **money shot**. Build toward it.

## Structure

Write `demo/script.md`:

- **Setup** — what's pre-staged before you share your screen: the environment, the repo,
  the tabs open, the seed data. Stage it all in advance so you can start cold.
- **The hook (one line)** — the customer's pain, said first. Not "let me show you our product."
- **The beats** — for each, three columns: *what you do*, *what they see*, *what you say*.
  Keep the saying about the outcome, not the clicks.
- **The money shot** — call it out. This is the moment that earns the next meeting.
- **The "so what"** — tie the result back to the outcome in their words, and name the next step.
- **Fallback** — a recorded clip or a pre-baked result to switch to if a live step fails.

## Rules

- **Pre-stage everything and never debug live.** A demo that breaks costs more than no demo.
- **One outcome per demo.** If you're showing three things, you're showing nothing.
- **Show real product behavior.** The output is real and the verifier checks it. If a step
  is pre-baked for time, know which one and keep the real version on hand.
- **Narrate the why, not the UI.** "Now it's catching the drift before it ships" beats "now
  I click here."
- **Time it.** A demo on a call has a budget; rehearse to it.

## Visuals

For a recorded or async demo, capture the run as a screen GIF or video so it doubles as the
fallback. Use the `claude-image-gen` skill for any title cards or diagrams.
