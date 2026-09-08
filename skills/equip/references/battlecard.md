# Battlecard recipe — value-framed and grounded

A battlecard arms the field for a competitive moment. The common failure is a feature
table that reads like marketing and falls apart when a customer pushes. EquipGTM
battlecards are built from the story manifest, so they lead with the outcome the customer
unlocks and back every claim with something the product can actually do.

## Structure

Generate these sections, in this order:

1. **The outcome we win on** — one sentence on the customer value this product unlocks
   better than the alternative. Pulled straight from the manifest `outcome`. Not a
   feature; a result.
2. **Where we win** — 3–4 plays, each tied to a manifest module: the customer situation,
   the capability that wins it, and the proof. Situation first, capability second.
3. **Discovery questions** — questions a rep asks to surface the pain this outcome solves.
   Each maps to a module's `customer_value`.
4. **Landmines** — honest places the alternative is weak for *this outcome*. State them as
   questions the customer can ask the competitor, not as insults.
5. **Objection handling** — the 3 objections this outcome attracts, each with a grounded
   response. If the honest answer is "we don't do that yet," say so and pivot to the
   outcome; a battlecard that overclaims loses the deal on contact.
6. **Proof points** — the concrete evidence from the manifest `proof` fields: the command
   that runs, the test that passes, the metric. These are what the verifier reproduces.

## Rules

- **Lead with the result, support with the feature.** Every claim is "the customer can
  now <do X>, because <capability>," never just "<capability> exists."
- **No unverifiable claims.** If a proof field is empty or the capability isn't in the
  product, the line does not ship. Run the verify gate before calling it done.
- **Name the competitor plainly, never sneer.** The field trusts a card that is fair more
  than one that is hype. Frame weaknesses as questions, not put-downs.
- **Keep it one screen.** A rep reads this between calls. Cut anything that isn't a play,
  a question, or a proof.

## Example play (one row of "Where we win")

```
Situation: The team finds entitlement drift in production, after customers do.
We win with: MCP grounding + a scheduled audit that opens fixes before release.
Proof: on the sample repo, the audit finds 2 drifts and opens a green PR.
```

That row leads with the customer's situation and outcome, names the capability second,
and ends with a proof a rep can actually show. Build every row that way.
