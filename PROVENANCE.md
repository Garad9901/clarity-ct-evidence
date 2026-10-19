# PROVENANCE - CLARITY-CT focused narrative review

Build tag for every number below: `evidence-v1.0` (set by CLAUDE CODE PROMPT 1).
Audit date: 19 October 2026. Every value was recomputed from the files listed, not copied from the draft.

| Number used in the paper | Value | File | How it is obtained | n | Coding |
|---|---|---|---|---|---|
| Records opened and verified | 147 | records/selected.json (84) + records/excluded.json (62) + records/gandomkar_2022_ref85.json (1) | count of records | 147 | single pass, AI-assisted |
| Sources included | 85 | records/selected.json + records/gandomkar_2022_ref85.json | count | 85 | single pass, AI-assisted |
| Included from 2025 or 2026 | 72 | records/selected.json, field `year` | year >= 2025 | 85 | derived from Crossref or publisher dates |
| Older included sources | 13 | as above (12 originals and standards + ref 85, 2022) | year < 2025 | 85 | derived |
| Preprints among included | 4 | records/selected.json, field `pub_type` | pub_type = preprint | 85 | derived |
| Records not included | 62 | records/excluded.json | count | 62 | single pass |
| Excluded: older beyond cap | 21 | records/excluded_reasons.csv | year < 2025 | 62 | derived |
| Excluded: preprints not essential | 13 | records/excluded_reasons.csv | pub_type = preprint | 62 | derived |
| Excluded: outside chest CT / not verifiable / redundant | 12 / 11 / 5 | NOT STORED PER RECORD | reasons for these 28 records were tallied in the session but not saved | 28 | [NEEDED: author re-assigns each reason in excluded_reasons.csv] |
| Studies in the evidence map | 27 | charting/table3_charting.csv | rows | 27 | single coder (AI); human double coding planned |
| Examples only or not stated / quantitative / expert rating or agreement / reader study | 15 / 7 / 3 / 2 | charting/table3_charting.csv, column `category_group` | count | 27 | single coder (AI) |
| Studies per family (attribution / concept / anatomical-case-counterfactual / report-grounded) | 12 / 4 / 6 / 5 | charting/table3_charting.csv, column `family` | count | 27 | single coder (AI) |
| Records verified / included per search theme | see supplement S5 | records/theme_*.json | count per theme file | 147 | single pass |
| Claim-citation pairs checked: supported / partly / not checked | 160 / 20 / 2 | verification/result_1..4.json | count of `verdict` | 182 | AI checkers; no supporting quotes stored |
| Bibliographic matches | 82 of 84 (2 fixed) | verification/result_1..4.json, field `biblio` | count | 84 | AI checkers |
| Fig. 5 values (0.60 vs 0 at F = 0) | computed | figures/figs.py | formula, equal weights, other components 0.8 | n/a | computation, no data |

Known provenance gaps (fix before Phase 10):
1. Exclusion reasons for 28 records are not stored per record.
2. Fig. 1, Fig. 3 and the graphical abstract contain typed-in numbers; Phase 9 scripts must read records/ and charting/ instead.
3. The search log (queries, dates, hit counts) was not kept; only opened records were recorded.
4. The citation check stored verdicts but no supporting quotes; Phase 6 redoes it with quotes.
evidence-v1.0 = a9101644ebb8d6feca0f80523e5796f8b36c5e98
