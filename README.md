# Rivet

News metadata, public records, and snapshot comparisons.

A current-events desk with two independent source lanes: current news metadata and related U.S. public records. Five topics: artificial intelligence, energy, trade, climate, and space. Pin a local snapshot; compare new links, changed metadata, and links absent from a later capped result set. Export and import timestamped JSON receipts, including source query URLs.

## Run locally

Node.js 22+ is required. No runtime dependencies or API keys.

```sh
npm start
# open http://127.0.0.1:4452
npm test
```

For deterministic Chrome checks: `npm install`, install Google Chrome, keep the server running, then `npm run test:browser`. Test fixtures are clearly marked and never shipped as live content. The downloadable ZIP contains the runnable server, adapters, browser assets, and tests. Run `npm start` after extracting it.

## API

`GET /api/brief?topic=ai` returns schema `rivet-snapshot/1`. Valid topics: `ai`, `energy`, `trade`, `climate`, `space`. GET only; unknown topics reject. No arbitrary upstream URL fetching. Each lane includes its provider identity, success/error state, query URL, retrieval timestamps, bounded items, and a scope description. HTTP 200 can contain one failed lane; inspect lane status. Both lanes failing returns HTTP 502 with the failure receipt. Invalid upstream bodies, timeouts, and oversize responses become explicit source errors.

Successful results cache for five minutes, with Vercel stale-while-revalidate up to ten more minutes. Partially successful results cache for one minute. Instance-local request coalescing reduces repeated upstream calls; this is not a distributed quota guarantee. This public prototype is not an SLA-backed news API or unlimited upstream proxy.

## Sources and clocks

- [GDELT DOC API](https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/): latest 60 matching indexed English-language links in 72 hours. Its indexing time is not a verified article publication time.
- [Hacker News Algolia API](https://hn.algolia.com/api): explicit fallback if GDELT fails; latest 60 matching story submissions in 72 hours. Community submissions are a different sample from general news. Submission time is labeled. The GDELT failure remains visible in the receipt. No comparisons are made across different provider indexes.
- [FederalRegister.gov API](https://www.federalregister.gov/developers/documentation/api/v1): latest 30 matching U.S. documents published in 90 days. Proposed rules, notices, final rules, and other types stay labeled. Search matches can be tangential. FederalRegister.gov is an informational XML rendition; use its linked official govinfo PDF when checking the legal record. No legal advice or official notice is provided.

A document matching a topic is not corroboration of any headline. The desk performs no article-body scraping, generated reporting, clinical assessment, political-bias rating, or truth scoring. Titles and linked content belong to their respective publishers. No claim of worldwide novelty is made.

## Snapshot semantics

Canonical exact URLs identify items; common tracking query parameters and fragments are removed. Reworded metadata means the title or document type differs. No article-body diff or correction is inferred. A departed item can have aged out, fallen outside the cap, or changed indexing; departure is not retraction. Failed lanes and changed provider indexes are excluded from counts. Comparisons pause when a pin is newer than returned cached data.

Snapshots are local to the browser, one pin per topic. Export before replacing a pin to preserve its history. There is no scheduled collector or server-side archive; the app checks when opened/refreshed. Browser storage can be blocked or cleared; imported receipts and in-memory pins still work for that visit. Exported receipts disclose topics and returned links. No analytics, paid APIs, accounts, cookies, or cloud profiles are implemented. Hosting and upstream providers see normal HTTP requests; publisher sites have their own privacy practices.

## Tests and limits

Core tests cover source adapters, tracking deduplication, query allowlisting, unsafe imports, bounded/invalid upstream bodies, partial failures, and fallback provenance. Browser tests use deterministic snapshots for pin/diff/export/import/persistence, search, failures, mobile overflow, and dialog keyboard closure. Live checks are separately recorded in `docs/live-validation.json`; they do not guarantee future upstream availability. GDELT rate limits and timeouts were observed during development and retained in the record. No screen-reader audit or longitudinal field study is claimed.

## Deploy

`public/` is static output; `api/brief.js` is the Vercel Node function. Configuration is in `vercel.json`. The loopback server runs the same handler locally. No secrets are needed. Deploy using the Vercel CLI or connect this repository in your Vercel account.

Code and original interface: MIT; see LICENSE. Self-hosted Inter has its own included font license. Upstream headlines and documents retain their respective rights and terms.
