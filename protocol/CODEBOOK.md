# Codebook (protocol-v1.0)

Code only what the study reports in the text you read. If the study does not say, code NR (not reported). Do not infer.

## 1. Screening decision (title-abstract and full text)

INCLUDE / EXCLUDE / UNSURE (title-abstract only). For EXCLUDE give the first reason that applies: E1 not chest CT; E2 no deep learning; E3 no explanation produced or evaluated; E4 not a primary study; E5 outside 2025-01-01 to search date; E6 not English; E7 duplicate or superseded by a peer-reviewed version; E8 insufficient information.

## 2. What counts as an explanation

Any output, shown to a person, that is meant to show why the model produced its prediction: attribution or saliency maps (Grad-CAM and variants, SHAP, LIME, integrated gradients, attention maps shown as explanations), predicted clinical concepts used for the decision, lobe- or region-level evidence, similar cases or prototypes, counterfactual images, or generated text linked to image regions. A segmentation mask that is itself the task output is not an explanation.

## 3. Family (one primary, optional secondary)

- A. Post hoc attribution maps: a map over the image computed after training (Grad-CAM, SHAP, LIME, integrated gradients, attention maps).
- C. Concept-based models: the model predicts named clinical descriptors and uses them for the output.
- S. Anatomically structured, case-based or counterfactual: evidence reported per lobe or anatomical region, retrieval of similar cases or prototypes, or counterfactual images.
- T. Report-grounded and vision-language: generated or retrieved text, with or without links to organs, regions or lesions.

If more than one applies, the primary family is the one the study evaluates; if none is evaluated, the one shown first in the results.

## 4. Assessment of the explanation (flags, then one category)

Set each flag to Y, N or NR:
- examples_shown: explanation outputs shown for selected cases.
- assess_quant: a number that measures the explanation itself (overlap with annotations such as IoU, Dice or pointing game; deletion or insertion curves; randomisation or sanity tests with a number; stability measures; concept accuracy against reference labels).
- assess_expert: one or more clinicians rate the explanations, or the study reports agreement between the explanation output and expert scoring, without measuring reader decisions.
- assess_reader: clinicians make diagnostic decisions with and without the explanation (or with different explanations) and an outcome is measured (accuracy, time, reliance or trust).

Category, by the highest flag present: R reader study > E expert rating or agreement > Q quantitative measure > X examples only > N not stated.

## 5. Model validation

- ext_test: Y if the model was tested on data from another institution, or a public dataset not used for training; T if only a later time period from the same institution; N if internal only; NR if not stated.
- patient_split: Y if the split is stated to be at patient level (or by scan series with one series per patient); N if split by slice or image, or stated not to be patient level; NR if not stated.

## 6. Read level

FULL (full text read), ABSTRACT (abstract only), PREPRINT (preprint version of a published paper read). Record the URL you read.

## 7. Worked rules for frequent cases

- A study that shows Grad-CAM for four cases and reports nothing else: family A, examples_shown Y, all assess flags N, category X.
- One radiologist rates maps on a 1-5 scale: assess_expert Y, category E.
- Deletion curve AUC reported for the maps: assess_quant Y, category Q.
- Radiologists read with and without the model's explanations, accuracy compared: assess_reader Y, category R.
- Training on 5,000 slices from 60 patients split 80/20 by slice: patient_split N.
