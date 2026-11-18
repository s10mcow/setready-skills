# SetReady agent skills

Free agent skills from SetReady for people putting a manufactured home on land, whether they will live in it, rent it out or sell it. Each skill interviews you in short rounds of numbered questions, looks up what it can, never calls a lot buildable or invents a price, and ends with a PDF you can hand to the pros you hire.

- **grill-my-land-deal**: Interviews you about the parcel, the home and the money until the plan holds up.
- **land-home-package-plan**: Picks up where the land grilling stops and plans the home, the site, the permits and the budget.

The plugin also adds the SetReady connector, which finds land-home pros such as installers, septic, well drilling, surveyors and lenders in Florida, Georgia, Alabama, South Carolina, North Carolina, Tennessee and Mississippi.

## Install

In Claude.ai, open Customize, then Plugins, choose Add, then Add marketplace, enter s10mcow/setready-skills and install SetReady. To find pros, connect SetReady from the plugin's Connectors tab.

In Claude Code:

```
claude plugin marketplace add s10mcow/setready-skills
claude plugin install setready@setready
```

## How to use it

Start with "should I buy this lot?" and give the county, the state, the price and your plan. When that PDF is done, start a new chat, attach it, and ask to plan the land-home package. The second skill also writes a spreadsheet of the budget, the permits and the open questions that you can edit as quotes come in.

## What data it sends

The skills run inside your agent and send nothing on their own. The PDF and spreadsheet scripts run where your agent runs and make no network calls. Your agent may browse public sources such as county GIS, FEMA flood maps, USDA soils and the Census Bureau to check facts. If you connect SetReady, a search for pros sends the county, the state and the kind of pro to SetReady. SetReady's privacy policy:

https://setready.us/privacy

## License

MIT. This repository is generated from the skills published at https://setready.us/skills and changes made here are overwritten.
