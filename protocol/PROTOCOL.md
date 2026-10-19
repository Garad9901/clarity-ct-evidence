# Pre-registered protocol: explanations for deep learning on chest CT, 2025-2026 (scoping review)

Version: protocol-v1.0, fixed on 19 October 2026 before any counted search was run.
Any change after this tag is recorded in DEVIATIONS.md with its date and reason; nothing is changed silently.
Reporting guideline: PRISMA extension for scoping reviews (PRISMA-ScR).
Registration: [NEEDED: OSF Registries DOI, added after registration and before the searches are run].

## 1. Research questions

- RQ1. Which families of explanation are produced for deep learning models whose input includes chest CT, in work published or first posted online from 1 January 2025 to the search date?
- RQ2. How was the explanation itself assessed in each study?
- RQ3. How was the underlying model validated (external test set; patient-level data split)?
- RQ4 (exploratory). Is assessment of the explanation beyond examples associated with external validation of the model?

## 2. Outcomes

Primary: the proportion of included primary studies whose explanation was assessed beyond examples (quantitative measure, expert rating or agreement, or reader study), with a Wilson 95% confidence interval.

Secondary:
1. Proportion of studies in each assessment category and in each family, each with a Wilson 95% CI.
2. Proportion with an external test set and proportion with a patient-level split, each with a Wilson 95% CI.
3. Inter-coder agreement: Cohen's kappa per coding pair for title-abstract screening, full-text eligibility, family, assessment category, external test set and patient-level split, each with a bootstrap 95% CI (2,000 resamples, seed 20261019).
4. RQ4: 2 x 2 table of assessment beyond examples (yes/no) against external test set (yes/no), with Fisher's exact test (two-sided, alpha 0.05) and the odds ratio with its 95% CI.

## 3. Sources and search strings (fixed)

Date window: 2025-01-01 to the search date. Language: English. The search date and the record count per source are recorded at run time in searches/SEARCH_LOG.md, and every raw export is committed unchanged in searches/raw/.

S1. PubMed (run through NCBI E-utilities by scripts/search_pubmed.py):
```
(explainab*[tiab] OR interpretab*[tiab] OR "XAI"[tiab] OR saliency[tiab] OR "Grad-CAM"[tiab] OR "class activation"[tiab] OR "Shapley"[tiab] OR "concept bottleneck"[tiab] OR "concept-based"[tiab] OR counterfactual*[tiab] OR "attention map"[tiab] OR "attention maps"[tiab] OR heatmap*[tiab] OR "heat map"[tiab] OR "heat maps"[tiab] OR "report generation"[tiab] OR "visual grounding"[tiab]) AND ("deep learning"[tiab] OR "neural network"[tiab] OR "neural networks"[tiab] OR "artificial intelligence"[tiab] OR "machine learning"[tiab] OR "foundation model"[tiab] OR "foundation models"[tiab] OR "vision-language"[tiab] OR transformer*[tiab]) AND (chest[tiab] OR thoracic[tiab] OR lung[tiab] OR lungs[tiab] OR pulmonary[tiab]) AND ("CT"[tiab] OR "computed tomography"[tiab]) AND 2025/01/01:2026/12/31[dp] AND english[la]
```

S2. IEEE Xplore (website, Advanced Search, Command Search; Publication Year 2025-2026; export all results as CSV):
```
("All Metadata":explainable OR "All Metadata":interpretable OR "All Metadata":XAI OR "All Metadata":saliency OR "All Metadata":"Grad-CAM" OR "All Metadata":"concept bottleneck" OR "All Metadata":counterfactual OR "All Metadata":"report generation") AND ("All Metadata":"chest CT" OR "All Metadata":"lung CT" OR "All Metadata":"thoracic CT" OR "All Metadata":"chest computed tomography" OR "All Metadata":"lung nodule" OR "All Metadata":"pulmonary nodule")
```

S3. arXiv (run through the arXiv API by scripts/search_arxiv.py; records first posted before 2025-01-01 are removed after download):
```
(abs:explainable OR abs:interpretable OR abs:saliency OR abs:"Grad-CAM" OR abs:"concept bottleneck" OR abs:counterfactual OR abs:"report generation") AND (abs:"chest CT" OR abs:"lung CT" OR abs:"thoracic CT" OR abs:"chest computed tomography" OR abs:"lung nodule" OR abs:"pulmonary nodule")
```

S4. The 147 records opened in the earlier non-systematic search (records/), added as an extra source and flagged as such in the flow diagram.

Context search (not part of the evidence map; used only to place 2025-2026 findings against earlier reader studies), PubMed:
```
(saliency[tiab] OR heatmap*[tiab] OR "heat map"[tiab] OR "heat maps"[tiab] OR explainab*[tiab] OR interpretab*[tiab] OR "Grad-CAM"[tiab] OR "class activation"[tiab]) AND ("reader study"[tiab] OR "observer study"[tiab] OR "observer performance"[tiab] OR radiologists[tiab]) AND (chest[tiab] OR thoracic[tiab] OR lung[tiab] OR pulmonary[tiab]) AND ("CT"[tiab] OR "computed tomography"[tiab]) AND ("deep learning"[tiab] OR "artificial intelligence"[tiab]) AND 2020/01/01:2024/12/31[dp] AND english[la]
```

Syntax correction rule: if a source rejects a string, the smallest change that makes it run is allowed once, before the counted run, and is recorded in DEVIATIONS.md.

## 4. Eligibility (fixed)

Include a record when all hold:
1. Published or first posted online from 2025-01-01 to the search date.
2. English.
3. Primary study of a deep learning model whose input includes CT of the chest (including low-dose CT and CT pulmonary angiography).
4. The study produces or evaluates an explanation of the model's output (CODEBOOK section 2). An explanation mentioned only as future work does not count.
5. Peer-reviewed journal or conference paper, or a preprint with no peer-reviewed version found (flagged).

Exclude, with the first reason that applies, in this order: E1 not chest CT; E2 no deep learning; E3 no explanation produced or evaluated; E4 not a primary study (review, editorial, protocol); E5 outside the date window; E6 not English; E7 duplicate or superseded by a peer-reviewed version; E8 insufficient information (neither the full text nor the abstract allows coding of family and assessment).

Reviews found by the search are not charted; they are listed for the comparison with earlier reviews.

## 5. Selection and coding process

Coders: all four authors, in two pairs. Pair 1: Om P. Gawande and Aditi A. Parshivanikar. Pair 2: Yash R. Garad and Vikas G. Bhowate.
Records are split at random between the pairs (scripts/merge_dedupe.py, seed 20261019).

1. Pilot: both pairs screen the same 20 randomly drawn records at title-abstract level and chart the same 5 included studies, compare, and fix CODEBOOK wording. Pilot records are then re-coded blind in the main round. If title-abstract kappa in a pair is below 0.60 after the pilot, a second pilot of 20 records is run and the codebook revision is logged.
2. Title-abstract screening: both members of a pair screen every record of their half independently (include / exclude / unsure). Unsure counts as include for full-text review.
3. Full-text eligibility: both members of the pair decide independently, with an exclusion reason from section 4.
4. Charting: both members chart every included study independently on sheets/charting_sheet.csv, using CODEBOOK definitions.
5. Disagreements: resolved by discussion within the pair; if unresolved, a member of the other pair decides. Labels before consensus are kept for the kappa calculation.
6. Independence: coders do not see each other's sheets until both are complete. No coder opens sealed/ before all coding is finished. No AI tool assigns, suggests or checks any label.

AI tools are used only to run the search scripts, remove duplicates, prepare blank sheets and compute the statistics in scripts/agreement_stats.py.

## 6. Sample size

The review is a census of all eligible records, not a sample. As a precision guide: for 50 included studies and a proportion near 0.5 the Wilson 95% CI half-width is about 13 percentage points; for 27 studies it is about 18 points. Proportions are always reported with their intervals.

## 7. Comparisons and sensitivity analyses

1. Comparison with the earlier map: how many of the 27 studies charted in evidence-v1.0 meet the eligibility criteria and are found by this search.
2. Comparison with published figures from earlier reviews (for example, the share of studies with no validation of the explanation reported in the scoping review of radiological cancer imaging cited in the article).
3. Sensitivity of the primary outcome: (a) excluding preprints; (b) excluding studies coded from the abstract only; (c) using each coder's labels before consensus.
4. Transparency item (supplement only, no claim): agreement between the AI labels in sealed/ and the human consensus labels for the studies present in both maps.

## 8. Statistics

- Proportions: Wilson score 95% CI.
- Agreement: Cohen's kappa per pair with bootstrap 95% CI (2,000 resamples, seed 20261019); Fleiss' kappa across all four coders for the pilot.
- RQ4: Fisher's exact test, two-sided, alpha 0.05; odds ratio with 95% CI (conditional maximum likelihood, scipy).
- Multiple comparisons: RQ4 is the only pre-specified inferential test, so no correction is applied to it. Any further test is labelled exploratory and Holm-corrected.
- Software: Python with the versions pinned in requirements.txt.

## 9. Tables to fill

- Table A. PRISMA-ScR flow: records identified per source; duplicates removed; screened; excluded at title-abstract; full texts assessed; excluded with reasons E1-E8; included.
- Table B. Included studies: study; family; task; data; explanation; assessment flags and category; external test set; patient-level split; read level.
- Table C. Kappa per pair and field, with 95% CI.
- Table D. Assessment category by family, counts and percentages with Wilson CIs.
- Table E. Assessment beyond examples by external test set (2 x 2), with Fisher p and odds ratio.

## 10. Timeline

Week 1: OSF registration, searches, deduplication, pilot, title-abstract screening.
Week 2: full-text eligibility and charting.
Week 3: consensus, statistics, Tables A-E, update of the claim ledger.
