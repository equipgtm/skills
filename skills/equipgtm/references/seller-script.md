# Seller-script recipe — start the conversation, across channels

Seller scripts give the field a way to open and advance the conversation about this use
case, in the channels they actually use: a discovery call, LinkedIn, and email. Every one
leads with the customer's outcome, never the product, and stays honest about what the
product can do.

## Rules for every channel

- **Lead with their outcome or pain, not your feature.** The first line is about them. The
  capability appears only as the route to the outcome, never as the opener.
- **One ask per touch.** Each script ends with a single, specific next step.
- **Grounded.** Any proof you cite is real — pull it from the manifest `proof` fields, and
  the verifier checks it. No invented results, no "industry-leading."
- **Short and human.** Respect the channel's length (below). A rep reads this between calls.
- Pull variables from the manifest: `<customer>`, `<vertical>`, `<pain>`, `<outcome>`,
  `<proof>`. Fill them where known; leave `<placeholders>` where the seller personalizes.

## The channels

Write `seller-script.md` with a section per channel, each a short adaptable template.

### Discovery call
- **Opener (≈15s):** name the outcome other `<vertical>` teams are chasing and ask if it's
  on their radar. No pitch yet.
- **Discovery questions (3–5):** each surfaces the `<pain>` the outcome solves, drawn from
  the manifest `starting_point`. Open and neutral, not leading.
- **Value line (one sentence):** "teams like yours use `<product>` to `<outcome>` — here's
  the proof: `<proof>`."
- **Close:** agree one concrete next step (a scoped demo, or a pilot on their repo).

### LinkedIn
- **Connection note (<300 chars):** one line of genuine relevance plus the outcome. No ask.
- **First message (after they connect):** two sentences — the `<pain>` you see in
  `<vertical>`, then the `<outcome>` — ending with a soft, low-friction ask.

### Cold email
- **Subject (offer 2–3):** outcome-led and specific, no hype or clickbait.
- **Body (3–4 sentences, under ~90 words):** their `<pain>` → the `<outcome>` → one
  `<proof>` point → one clear CTA.

### Follow-up email (after a call or demo)
- Reference the specific thing discussed, restate the `<outcome>` in their words, point to
  the `<proof>` they saw, and propose the next step.

## Honesty note

A script that overclaims burns the rep's credibility on the call, which is far more
expensive than a softer claim. If the honest answer to a likely question is "not yet,"
script the pivot back to the outcome rather than bluffing. Run the verifier on any
capability or proof a script cites, the same as any other artifact.
