# Rivet — Public comment planner

Find U.S. proposed rules with listed future comment dates, save deadlines, and prepare a sourced response. This is a participation workbench, not a news feed. Official submission takes place outside Rivet, through the agency’s linked route.

## Use it

1. Search a policy term or browse keyword-based topic filters. Narrow by agency or dates due within 7/30 days. A visible, reversible filter hides routine aircraft/airspace items by default; saved workspace records are always shown.
2. Open a record to read the agency’s abstract, date instructions, docket IDs, and official PDF. Verify exact cutoff and amendments.
3. Save the record. Write a specific issue, citation, experience, evidence, and requested change in the local draft form.
4. Export a draft or calendar preparation reminder. Follow the official comment route to submit your reviewed response yourself. Rivet never submits it.
5. Export a workspace backup to keep or transfer your records and drafts. Submitted status is self-reported, not verified.

## Run locally

Requires Node.js 22+. No runtime dependencies, API keys, or paid services.

```sh
npm start
# http://127.0.0.1:4452
npm test
```

For deterministic browser checks: install Google Chrome, run `npm install`, start the server, and run `npm run test:browser`. The tests use clearly marked fixtures; live provider checks are recorded separately in `docs/live-validation.json`.

## API

`GET /api/opportunities` returns `rivet-opportunities/2` with a source query URL, retrieval time, provider total, and up to 200 normalized records. `?q=water` performs an upstream search (100-character limit). `?id=2026-12345` retrieves one supported proposed rule with a listed comment date, even if its date has passed. GET only; arbitrary provider URLs and invalid IDs reject. Provider errors return 502 instead of pretending there are zero opportunities. Successes cache for five minutes plus up to five minutes of stale-while-revalidate on Vercel. Instance-local coalescing and a 60-entry cache reduce repeated requests; there is no distributed quota guarantee or uptime SLA.

The earlier news API `/api/brief` now returns HTTP 410 and points to this replacement. News snapshots from version 1 are not workspace backups and cannot be imported. Existing version-1 browser data is not deleted. Old releases remain available in GitHub history/releases.

## Source and deadline contract

The [Federal Register API](https://www.federalregister.gov/developers/documentation/api/v1) is queried with `conditions[type][]=PRORULE`, `conditions[comment_date][gte]` set to today in America/New_York, `order=newest`, and `per_page=200`. Explicit fields include the abstract, deadline, docket IDs, comment URL, PDF, and agency date instructions. Rows are validated and rechecked against the current date. Default results are locally sorted by listed deadline.

This is a bounded set of the **newest** matching proposed rules, not a complete register of participation opportunities. It excludes notices, state/local processes, unsupported documents, and unknown comment dates. Keyword labels are transparent string matches, not AI relevance judgments. Search the provider to narrow a large result set. Provider totals can exceed displayed results due to the cap, validation, or a date boundary.

A future date does not independently verify that a docket is accepting comments. Read current amendments, exact cutoff, and official submission instructions. FederalRegister.gov is an informational rendition; the linked govinfo PDF is the official edition. Direct comment URLs are used only when supplied by the source and on an allowlisted official host. Source-provided HTTP links are upgraded to HTTPS only on those hosts. Without a comment URL, Rivet links the official document’s instructions instead of inventing a submission link.

Calendar exports are all-day **preparation reminders one day before** the listed date, with exclusive end dates. They do not promise a closing time. Same-day/past reminders are not exported. Deadline math uses calendar dates and Eastern Time, not an invented 24-hour countdown.

## Drafting and privacy

Prompts reflect [HHS public-comment guidance](https://www.hhs.gov/sites/default/files/regulations/rulemaking-tool-kit.pdf): identify a provision, cite it, support your reasoning, and propose a specific change. The six-item checklist measures completeness only, not factual accuracy, legal sufficiency, or likely influence. No arguments, impact estimates, or evidence are generated. Nothing is submitted automatically. This is not legal advice or an official government service.

Saved records and drafts stay in browser local storage. No accounts, analytics, model APIs, or server draft database. Anyone sharing the browser or opening an exported backup can read drafts. Browser storage can be unavailable/cleared. Export backups before switching devices. Imports merge new records and preserve existing drafts. Cross-tab changes pause an open editor so stale drafts cannot silently overwrite another tab. Source metadata for saved rules is refreshed when present in a successful query, without changing draft text.

Public comments submitted to official portals may become public, including personal information in the text. Review that portal’s terms. Hosting and upstream providers receive normal requests; search terms are sent to the provider. Remove a saved record or clear site data to delete local drafts; downloaded files remain separate.

## Validation and deployment

Core/API tests cover Eastern Time/DST boundaries, invalid deadlines, safe official links, input limits, bounded provider errors, backup validation, non-generated exports, and UTF-8 calendar folding. Browser tests cover saving, writing, cited exports, reminders, reload persistence, cross-tab edit protection, backup rejection, search/filtering, mobile dialogs, and absence of automatic submissions. No screen-reader audit, actual comment submission, policy-outcome validation, or independent scientific study is claimed.

Static output is `public/`; `api/opportunities.js` is the Vercel function. `server.mjs` uses the same handler locally. Build a deterministic local-app archive with `python3 scripts/package.py`. Previous UI and news validation records are retained under `docs/history/` and do not validate the new planner.

Code/original interface: MIT. Inter font has its included license. Government source content retains its original status. No worldwide-novelty claim is made.
