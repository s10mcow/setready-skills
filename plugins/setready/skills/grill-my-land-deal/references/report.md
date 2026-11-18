# The PDF report

Make the report once the user confirms the summary. The user keeps it and hands it to the
pros named in it, so write it for someone who missed the conversation.

## How to make it

1. Write the confirmed summary to `report.json` in the shape below.
2. Run the layout script in this skill's references folder:

   ```
   python3 references/report.py report.json land-deal-<county>-<state>-<date>.pdf
   ```

   Name the file in lowercase with hyphens, for example
   `land-deal-berkeley-sc-2026-11-17.pdf`.
3. In Claude.ai, give the user the PDF to download. In Claude Code, leave it in the current
   folder, delete `report.json`, and give the path.

The script needs reportlab. If it says reportlab is missing, run `pip install reportlab` and
try again. If that fails, make a PDF another way with the same sections in the same order.
If you can't make a PDF at all, write the same report as a Markdown file and say why.

## What goes in report.json

```json
{
  "title": "Land deal summary",
  "subtitle": "201 Example Rd, Town · Parcel 123-45-678 · Example County, SC",
  "meta": [["Date", "2026-11-17"], ["Goal", "Sell the land and home together"], ["Asking price", "$59,500"]],
  "sections": [
    {"kind": "flags", "title": "Red flags", "tone": "red", "tile": true,
     "empty": "None found in this conversation.",
     "items": [{"title": "No recorded access to a public road",
                "detail": "The plat shows a dirt road but no easement for this lot.",
                "status": "Red flag",
                "evidence": "Recorded plat, Plat Book 1, Page 2; county GIS, read 2026-11-17",
                "who": "Title services; surveyor"}]},
    {"kind": "table", "title": "Open questions", "tone": "amber", "tile": true,
     "columns": ["Question", "Who answers it", "Why it matters"], "widths": [46, 24, 30],
     "rows": [["Will the county allow a manufactured home here?", "County planning or zoning office", "If not, there is no home permit."]]},
    {"kind": "list", "title": "Settled", "tone": "green", "tile": true,
     "items": ["**Goal:** sell the land and a new home together."]},
    {"kind": "table", "title": "What was looked up", "status_column": 1,
     "columns": ["Fact", "Status", "Source", "Date read"], "widths": [40, 17, 30, 13],
     "rows": [["Flood zone X", "Verified", "[FEMA flood map](https://msc.fema.gov)", "2026-11-17"]]},
    {"kind": "text", "title": "Next step", "callout": true,
     "paragraphs": ["**Plan the package.** ...", "**Find the pros named above** ... https://setready.us/directory"]}
  ],
  "footer": "Not a survey, title search, appraisal, or legal, tax or lending advice.",
  "closing": ["Made with grill-my-land-deal, a free agent skill from SetReady", "https://setready.us/skills"]
}
```

- **subtitle:** the address or parcel number, the county and the state, joined with " · ".
- **meta:** the date, the user's goal (live in it, rent it out or sell it), and the asking
  or target price if the user gave one.
- **Red flags:** a short title of ten words or fewer, then the detail, the status from
  references/evidence-status.md, the evidence (source and date read) and who can confirm or
  clear it, named from references/pro-roles.md. With none, keep the section and leave
  `items` empty.
- **Open questions:** who answers each one is a kind of pro or office, or "You".
- **Settled:** each decision in one line.
- **What was looked up:** every fact with its status, its source as a link when there is
  one, and the date read. Leave the section out if nothing was looked up.
- **Next step:** first, that the next skill is land-home-package-plan, which plans the home,
  the site, the permits and the budget and starts from this PDF. Then, in SetReady's seven
  states, that the pros named above are in SetReady's directory, with its link. Outside
  those states, the kinds of pro to look for locally.
- **footer** and **closing:** exactly as shown.

Text can use `**bold**` and `[label](link)`.

## Rules

- Put nothing in the PDF that isn't in the summary the user confirmed.
- The conversation's rules hold here too: never say the parcel is buildable or the deal is
  good, give no price the user or a source didn't give, and show every fact with its status.
