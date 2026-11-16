---
name: literature-verification
description: Verify a literature item before relying on it - raise roadmap or plan entries marked [S] (search snippet / second-hand) or [U] (unverified) to [V] by checking the primary source (arXiv abstract or HTML page, journal DOI page, official data release page) for authors, year, identifiers, the exact numbers with their uncertainties and units, and data product names and sizes; record what was checked and where. Use before citing, reproducing or pre-registering against any paper number, and whenever a reference looks wrong or cannot be found.
---

# Literature verification ([S]/[U] to [V])

Rules live in `AGENTS.md` (section 2 "引用前先核实" and the paper-study reading rule; section 1
for data sizes). The markers are defined at the top of `ROADMAP.md`. This skill is the order of
work and the checklist.

## 1. List what needs checking

- Collect every item the task will rely on: references, numbers, data products, dates. Take the
  marker from `ROADMAP.md`, the design plan or the study README; anything without a marker counts
  as [U].
- Only numbers that the study will compare with, cut on or quote need [V]; say which ones you
  are leaving at [S]/[U] and why.

## 2. Check each item against the primary source (read only)

- Use web search to find the source, then read the page itself: arXiv abstract or HTML page,
  the journal's DOI page, ADS, the data centre's landing or documentation page. A search snippet,
  a press release, a review or another paper's citation is not a primary source: at best [S].
- Never download the paper or a data file into the project (AGENTS.md section 1); reading a
  PDF page in the browser is fine.
- **Identity**: the arXiv id resolves to the stated title and first author; year and journal
  reference (volume, page or article number) match; the DOI resolves to the same paper. A
  mismatch here often means a wrong or invented reference: search by title and author instead of
  trusting the id.
- **Numbers**: the value, its uncertainty and what kind it is (1σ, 68 % or 95 % interval,
  posterior median or best fit), units and conventions (h-scaling, magnitude system, epoch,
  fixed versus marginalised parameters), and where it sits (section, table, equation, figure).
  Note the arXiv version (v1 and the published version can differ) and errata.
- **Data products**: exact name, version or DOI, file names and stated sizes from the landing
  page or a server-side `COUNT(*)` (`server-side-query` skill), never by downloading to find out.
- **Quotes**: copy verbatim only the short quotes the work needs (for `[stated]` premises in a
  paper study); paraphrase the rest.

## 3. Record

- Change the marker to [V] where the item is listed (`ROADMAP.md`, the plan, the study README)
  and add the identifier or page that confirms it, e.g. `arXiv:2404.03002, Table 3 [V]`.
- Items that disagree with the source: correct them in place and say what changed in the plan's
  execution record or the study's `log.md` (Chinese, English terms in parentheses).
- Items that cannot be confirmed stay [S]/[U] with the reason ("no public table", "only in a
  talk"); do not build a pre-registered criterion on them without telling the user.
- Later literature that changes a number is recorded as such (with its own id), not merged
  silently into the original paper's value.
