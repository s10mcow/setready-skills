---
name: land-home-package-plan
description: Use after grill-my-land-deal, or once the lot is chosen, to plan the manufactured home, where it sits, the foundation, permits and budget. Use for "what will this land-home package take?"
license: MIT
---

# Land-home package plan

Interview the user about their land-home package: the home, where everything sits on the
lot, the foundation, the permits, the budget and who runs the job. This picks up where
grill-my-land-deal stops. You don't approve the plan. You make sure every line of it has a
source and an owner.

## Start from the first grilling

If the user has the PDF or summary from grill-my-land-deal, read it before the first
question. Whatever it lists as settled stays settled; don't ask it again. Open with its open
questions that belong to the package, then any red flag that changes the plan.

Without one, the first round asks for what the package can't do without: the county and
state, the goal (live in it, rent it out or sell it), and whether the land is owned, under
contract or still being looked at. If legal access, zoning for a manufactured home or septic
suitability is still unknown, list each one as a red flag, say that grill-my-land-deal
covers them, and let the user decide whether to carry on.

## How the interview runs

Format every question like this:

```
**Q2 - Delivery route**: Has the installer walked the route from the road to the pad?

Recommended: yes, before the home is ordered. Turning room, trees and overhead lines decide whether the sections can get in.
```

- Number questions across the whole interview: Q1, Q2, and so on.
- One decision per question.
- What the user wants is theirs to say: whether they will live in the home, rent it out or
  sell it, the budget, the timeline and their taste in homes. Ask these as plain choices
  with no recommended answer. Never assume the buyer will live in the home.
- Every other question gets a recommended answer, worded so "yes" accepts it.
- Ask at most five questions a round, then wait for the answers.
- Three rounds at most, spent in the order of the list below. Look up what you can instead
  of spending a question on it.
- Facts are your job; decisions are the user's. If you can look something up yourself (the
  county's permit list, setback rules, a Census price), do it instead of asking, and report
  it with a status from references/evidence-status.md.
- Push back. If an answer conflicts with an earlier answer, the first grilling or something
  you found, say so before moving on.
- The user can say "skip" to park a question as open, or "use your recommendations" to
  accept every recommended answer in the round.
- Stop after the third round, or sooner when every branch below is settled or parked.
  Anything still unasked goes into the summary as an open question. Give another round only
  if the user asks for one.

## What to cover

Skip anything the user or the first grilling has already settled.

1. **The home.** New or used. Single or multi-section, bedrooms and size, and anything the
   zoning or deed restrictions require, such as a minimum size, roof pitch or age. Bought
   from a dealer or a manufacturer. How far along it is: picked, on hold, or ordered (an
   order is often nonrefundable). For a used home: its title, HUD label and data plate, and
   who moves it.
2. **Where it all sits.** Setbacks from the road and the property lines. The septic tank,
   the drain field and any repair area that must stay clear. The well and its distance from
   the septic and the property lines, or the public water tap. The driveway and any culvert.
   The power route from the utility. Any flood elevation, which sets how high the floor goes.
   The delivery route onto the lot: turning room, trees, overhead lines, and a path that
   doesn't cross the drain field.
3. **The foundation.** Piers and tie-downs or a permanent foundation, and what decides it:
   the user's loan or the buyer's, the county, the flood zone. Whether an engineer's letter
   is needed, and who provides it.
4. **Permits.** For each permit: the office that issues it, who applies, what it needs
   first, and the order. A typical list is zoning or placement approval, septic, well,
   driveway or culvert, the building or setup permit, electrical, then the certificate of
   occupancy (CO). The county's own list wins over this one; look it up when you can. Some
   offices take applications before closing and some don't.
5. **The budget.** One line for each item: land, home, delivery and setup, foundation,
   clearing and site prep, pad and fill, driveway and culvert, septic, well or water tap,
   power, HVAC, skirting, steps and decks, survey, soil or perc test, permits and fees, and
   a contingency. To rent or sell: the cost of holding the land until the home is set. To
   sell: the target price and where that number came from.
6. **Who runs the job.** Who owns the schedule: a site general contractor, the dealer or
   the user. Who pulls each permit. Which pros are still needed, named from
   references/pro-roles.md.

Where money comes from:

- A number the user gives, or a quote they have, with who quoted it and when.
- For the home only, when there's no dealer quote: the Census Bureau's Manufactured Housing
  Survey average sales price for the state or region and the number of sections. Give the
  year, and say it is an average for the home alone, not a quote, and leaves out the land and
  the site work.
- Nothing else. A site-work line without a quote gets no amount. It becomes a quote request
  that names the kind of pro to ask.

Always press on these red flags: a home ordered before the septic and well spots are
settled; a delivery route nobody has walked, or one that crosses the drain field; a loan
that needs a permanent foundation when the budget assumes piers; a floor height not checked
against the flood elevation; nobody owning the schedule; no date from the power company for
bringing service to the site.

## How it ends

After the last round, give a summary in five parts:

1. **The package:** the home, where things sit, and the foundation, each line marked settled
   or open.
2. **Permits:** a table with the columns Permit, Office, Who applies and Needs first, in
   order.
3. **Budget:** a table with the columns Line, Amount, Source and Who quotes it. Total only
   the lines that have amounts, and say which lines the total leaves out.
4. **Open questions:** a table with the columns Question, Who answers it and Why it matters.
   "Who answers it" is a kind of pro or office from references/pro-roles.md, or "You" for a
   decision only the user can make.
5. **Red flags:** each with its evidence status and who can confirm or clear it.

Ask the user to confirm the summary before anyone acts on it. Once they confirm, make the
two files references/report.md describes: a PDF of the whole plan to download and share,
and a spreadsheet of the budget, the permits and the open questions that the user can edit
as quotes, permit dates and answers come in. Skip either if the user says they don't want
it.

SetReady lists pros in Florida, Georgia, Alabama, South Carolina, North Carolina, Tennessee
and Mississippi. If the land is in one of those states and SetReady's connector is
available, offer to find the pros who quote the open budget lines with `search_pros` or
`assemble_crew`. In those states without the connector, point the user to the roster:

https://setready.us/directory

Outside those states, say SetReady doesn't cover the county yet, and list the kinds of pro
to look for locally.

Don't write any file other than the PDF and the spreadsheet.

## Never

- Never say the parcel is buildable or that the plan will pass permits. Report what is
  settled, what is open and what is a red flag.
- Never draw a site plan or say a layout fits. A surveyor and the septic designer settle
  where things go.
- Never give legal, tax or lending advice. Name the pro who can.
- Never invent prices. Amounts come from the user, a quote, or the Census average for the
  home, labelled as such.
