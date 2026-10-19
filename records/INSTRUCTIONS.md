# Literature search instructions (read fully before starting)

You are collecting REAL, VERIFIED references for a narrative review article to be submitted to the
Journal of Imaging Informatics in Medicine. Topic of the review: explainable AI (XAI) for deep learning
on chest CT. Research integrity matters more than quantity: a made-up or mis-described reference would be
research misconduct for the authors.

## Hard rules
1. Include a paper ONLY if you opened a page for it in this session (publisher landing page, PubMed Central
   full text, arXiv/alphaXiv page, or its Crossref record) and saw its title and authors there.
   Never add a paper from memory. Never guess a DOI, volume, page number or author list.
2. Every field you record must come from a page you opened. If a field is not shown, write null.
3. "key_finding" must describe what THIS paper actually reports, in your own words, based on its abstract or
   full text that you read. No copied sentences. Include concrete specifics (dataset, cohort size, method,
   headline number) when the abstract gives them. If you only saw the title and not the abstract, write
   "abstract not read" and set abstract_read to false.
4. Date policy: at least 85% of your papers must be published in 2025 or 2026 (online-first date counts).
   Older papers are allowed only where listed below as "essential originals".
5. Prefer peer-reviewed journal articles and major conference papers (MICCAI, CVPR, NeurIPS, ICLR, MIDL, ISBI).
   arXiv preprints are allowed only when the work is important and has no published version; mark them.
6. Exclude: predatory or non-indexed journals, retracted papers, papers not about the theme, duplicates.
   Check each landing page for a retraction or expression-of-concern notice and exclude if present.

## How to search and verify (practical notes for this environment)
- Tools: WebSearch (use mode "standard"; "extended" for hard cases), WebFetch, and the alphaXiv tools for arXiv
  papers (load them with ToolSearch query "select:mcp__alphaXiv__discover_papers,mcp__alphaXiv__answer_pdf_queries,mcp__alphaXiv__get_paper_content").
- WebFetch rejects URLs longer than about 250 characters. Keep URLs short.
- Verify metadata with Crossref: WebFetch https://api.crossref.org/works/<DOI> and read title, author list,
  container-title, short-container-title, volume, issue, page or article-number, published date, type.
  A Crossref search also works: https://api.crossref.org/works?query.bibliographic=<words>&rows=10&filter=from-pub-date:2025-01-01&select=title,DOI,issued,container-title,author
- Sites that usually work: api.crossref.org, pmc.ncbi.nlm.nih.gov (full text), link.springer.com article pages,
  nature.com, mdpi.com, frontiersin.org, pubs.rsna.org, arxiv.org, alphaxiv.org, bmj.com, jmir.org.
- Sites that usually fail: sciencedirect.com, PubMed search pages, Europe PMC API, OpenAlex API, IEEE Xplore,
  Wiley. For papers on those sites, read the abstract from PMC, arXiv, or a Crossref record that includes it.
- If a request returns HTTP 429 (rate limited), do not retry that URL; move on to another source.
- Do not use curl or any shell networking; it is blocked.
- Lessons from earlier searches in this session: pmc.ncbi.nlm.nih.gov and PubMed now return a browser-check page,
  so do not rely on them. Crossref returns HTTP 429 when several queries are sent at once: send Crossref requests
  ONE AT A TIME, not in parallel. WebSearch has a shared budget that may run out; if it stops working, discover
  papers with Crossref bibliographic search, alphaXiv discover_papers, and journal article pages on
  link.springer.com, nature.com, mdpi.com, frontiersin.org, pubs.rsna.org, bmcmedimaging.biomedcentral.com.
- Cap your file at 18 papers. Quality and verification over quantity.

## Output
Write a JSON file at the path given in your task. It must be a JSON array of objects with exactly these keys:
  "authors": list of strings, every author in order, each as "Surname Initials" without periods (e.g. "Koh PW").
             If the page shows only some authors, list those you saw and set "authors_complete": false.
  "authors_complete": true/false
  "title": exact title as shown
  "journal": full journal or proceedings name
  "journal_abbrev": Crossref short-container-title or NLM abbreviation if you saw it, else null
  "year": publication year (print/issue year if assigned, else online year)
  "online_date": first online date if shown, else null
  "volume", "issue", "pages": strings or null ("pages" may be an article number)
  "doi": string or null
  "url_opened": the URL(s) you actually opened for it
  "pub_type": "journal" | "conference" | "preprint" | "guideline" | "book"
  "is_review": true/false
  "abstract_read": true/false
  "key_finding": 1-3 sentences, your own words
  "use_for": which part of the review it supports (short phrase)
  "verified_how": e.g. "Crossref record + PMC full text"
  "flags": any doubt, mismatch between sources, or missing field (string, "" if none)
Validate the file with: python3 -c "import json;print(len(json.load(open('<path>'))))"

## Final reply
Reply with: the number of papers saved, how many are 2025-2026, a compact list (first author, year, short
title, journal) and an honest list of anything you could not verify or searches that failed. Do not include
papers in the reply that are not in the file.
