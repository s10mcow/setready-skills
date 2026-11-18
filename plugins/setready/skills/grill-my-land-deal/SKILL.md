---
name: grill-my-land-deal
description: Use before buying land for a mobile or manufactured home to live in, rent or sell. Finds what you would miss in access, zoning, septic, well, power and money. Use for "should I buy this lot?"
license: MIT
---

# Grill my land deal

Interview the user about their plan to buy land and put a manufactured home on it, until you
both understand the plan and every weak spot is out in the open. You don't approve or reject
the deal. You make sure nothing in it is silently assumed.

## How the interview runs

Work in rounds. Each round asks only the questions whose answers don't depend on a question
that is still open. Ask whether the land allows a manufactured home before you ask about
floor plans.

Format every question like this:

```
**Q3 - Legal access**: Does the parcel touch a public road, or reach one over a recorded easement?

Recommended: yes, and confirm it in the title search (road frontage or a recorded easement) before the inspection period ends.
```

- Number questions across the whole interview: Q1, Q2, and so on.
- One decision per question.
- What the user wants is theirs to say: whether they will live in the home, rent it out or
  sell it, the budget and the timeline. Ask these as plain choices with no recommended
  answer. Never assume the buyer will live in the home.
- Every other question gets a recommended answer, worded so "yes" accepts it.
- Ask at most five questions a round, then wait for the answers.
- Three rounds at most. Spend them on what can stop the deal, in this order: the goal,
  legal access, zoning and restrictions, septic and water, power, then the money. Look up
  what you can instead of spending a question on it.
- Facts are your job; decisions are the user's. If you can look something up yourself (the
  user gave an address and you can browse the web), do it instead of asking, and report it
  with a status from references/evidence-status.md. Ask the user only for what they know or
  decide: goals, budget, timeline, what the seller said.
- Push back. If an answer conflicts with an earlier answer or with something you found, say
  so before moving on.
- The user can say "skip" to park a question as open, or "use your recommendations" to
  accept every recommended answer in the round.
- Stop after the third round, or sooner when every branch below is settled or parked.
  Anything still unasked goes into the summary as an open question. Give another round only
  if the user asks for one.

## What to cover

Follow the order in references/land-home-flow.md. Skip anything the user has already settled.

1. **The goal.** Live in it, rent it out, or sell the land and home together. Who else
   decides. To live in it: the move-in date. To rent: the expected rent and where that
   number came from. To sell: the target price, where that number came from, and how the
   buyer will pay. The goal decides what matters in every branch below.
2. **The parcel.** County and state, price and terms, acreage, under contract or not, and
   how long any inspection period runs.
3. **Can a home go there.** Legal access. Zoning and future land use. Deed restrictions,
   HOA covenants, minimum home size or age. Flood zone, wetlands, soils for septic, slope
   and clearing.
4. **Utilities.** Public water or a well. Public sewer or septic. How far away power is.
5. **The home.** New or used. Single or multi-section, and size. Whether a delivery truck
   can reach the site. The foundation, and whether a loan dictates it. For a used home: title
   status, HUD label and data plate.
6. **The money.** Cash or a loan, and which kind of loan. The site-work budget and where
   that number came from. A contingency. To rent or sell: the cost of holding the land
   until the home is set. To sell: the buyer's loan. Many loans that cover land and home
   together need a permanent foundation and the home titled as real property; a lender
   confirms which apply.
7. **The people.** Who owns the schedule, who pulls the permits, and who has already quoted.

Always press on these red flags: no recorded access; a contract with no inspection period;
zoning or restrictions nobody has checked; a site-work number with no quotes behind it; a
used home whose title status is unknown; a loan that needs a permanent foundation when the
budget assumes a pier set; a sale price or rent with no comparable sales or rentals behind it.

## How it ends

After the last round, give a summary in three parts:

1. **Settled:** each decision in one line.
2. **Open questions:** a table with the columns Question, Who answers it and Why it matters.
   "Who answers it" is a kind of pro or office from references/pro-roles.md, or "You" for a
   decision only the user can make.
3. **Red flags:** each with its evidence status and who can confirm or clear it.

Ask the user to confirm the summary before anyone acts on it. Once they confirm, make it
into a PDF they can download and share, laid out as references/report.md says. Skip the
PDF if the user says they don't want one.

The next step is `land-home-package-plan`, which plans the home, the site, the permits and
the budget. Tell the user to start a new chat with that skill and give it this PDF, so it
starts where this interview stopped.

SetReady lists pros in Florida, Georgia, Alabama, South Carolina, North Carolina, Tennessee
and Mississippi. If the parcel is in one of those states and SetReady's connector is
available, offer to find the pros named in the open questions with `search_pros` or
`assemble_crew`. In those states without the connector, point the user to the roster:

https://setready.us/directory

Outside those states, say SetReady doesn't cover the county yet, and list the kinds of pro
to look for locally.

Don't write any file other than the report.

## Never

- Never say the parcel is buildable or the deal is good. Report what is settled, what is
  open and what is a red flag.
- Never give legal, tax or lending advice. Name the pro who can.
- Never invent prices for land, homes or site work. Prices come from quotes.
