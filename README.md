# unifesp-bodypart-benchmark

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24027438.svg)](https://doi.org/10.5281/zenodo.24027438)

**How reliable are radiograph body-part classifiers?** A leakage-controlled, cross-dataset benchmark with reliability and label-quality analysis on public data.

Authors: Sheikh Noor Abdullah (first author), A.B.M. Kabir Hossain. Department of Information and Communication Engineering, Bangladesh Army University of Engineering & Technology (BAUET), Natore, Bangladesh.
Status: manuscript in preparation. Funding: none.

> This repository makes **no state-of-the-art claim**. Its contribution is a transparent evaluation protocol, honest negative results and reliability tools.

## What is in the study
* **Protocol:** patient-level multilabel-stratified split of the UNIFESP body-part dataset (22 classes, 1,738 labelled radiographs, 768 patients), a fixed held-out set (323 images / 156 patients), all choices (head/TTA variant, ensemble weights, thresholds) made on out-of-fold predictions only, patient-level bootstrap CIs.
* **Experiments:** ablations (augmentation, loss, backbones, seeds, CNN-Transformer fusion, split type), frozen foundation-model probe, MURA body-part benchmark, zero-shot transfer to MURA / FracAtlas, COVID-19 Radiography (image-level split), calibration and selective prediction, out-of-fold label audit, Grad-CAM faithfulness checks, Kaggle late submissions.

## Key results (all numbers come from files in `results/`; see `docs/PAPER_FACTS.md`)
| Item | Result |
|---|---|
| Held-out ensemble (UNIFESP) | sample-F1 0.9189 [0.8669, 0.9602]; ensemble minus best single model +0.0066 [-0.0002, +0.0142], p = 0.063 |
| Ablations | no configuration significantly better or worse than the reference (all p > 0.08) |
| Evaluation shortcuts | random image-level split over-estimates validation F1 by 0.0144 (patient-level 0.0004); thresholds tuned on the held-out set add +0.0083 |
| Fusion gate | CNN-branch weight 0.0000 / 0.0029: the gate collapses onto one branch |
| Frozen DINOv2-S + linear probe | held-out 0.8859 [0.8327, 0.9318] |
| MURA body part (official validation split) | accuracy 0.9747 [0.9663, 0.9818], macro-F1 0.9707 |
| Reliability | ECE 0.0545 (already calibrated); 94.5 % accuracy at 90 % coverage |
| Label audit | 39 of 1,415 training images (2.8 %) flagged as suspected label errors (not clinician-reviewed) |
| Kaggle (late submissions, not ranked) | private 0.92563 (Stage 1) and 0.92638 (Stage 2); would fall between 2nd (0.92787) and 3rd (0.92488); #1 is 0.93378 |
| Stage 2 OOF (all 1,738 images) | plain 0.9262, pseudo-labelled 0.9233, union 0.9279; differences not significant |

## Repository layout
| Path | Content |
|---|---|
| `v2/src/` | all Python modules (data, training, ensembling, evaluation, ablation report, transfer, probe, reliability, Grad-CAM) |
| `notebooks/` | **reusable Kaggle notebooks**: `ready_to_run/` (final) and `earlier/` (provenance); see `notebooks/README.md` |
| `v2/*.ipynb`, `v2/build_*.py` | Kaggle notebooks (generated from `v2/src`) and their builders; `v2/test_*.py` unit tests |
| `evalkit.py`, `eda.py`, `stage2_ci.py` | evaluation toolkit, dataset EDA, Stage 2 bootstrap CIs |
| `make_paper_tables.py`, `make_figures.py`, `make_latex.py`, `build_docx.py` | tables, figures, LaTeX and Word manuscript builders |
| `results/` | printed outputs and CSVs from the Kaggle runs (`results/kaggle_raw/` = files downloaded from public notebooks) |
| `figures/`, `latex/`, `submission/` | paper figures (PNG + PDF), Overleaf-ready LaTeX, cover letter / highlights / title page |
| `MANUSCRIPT_v2.md` | working manuscript text |
| `docs/` | verified citations, dataset provenance and licence checks, the table of every number used in the paper (`PAPER_FACTS.md`), runbook |

## Data (not included)
| Dataset | Source | Terms |
|---|---|---|
| UNIFESP X-Ray Body Part Classification | https://www.kaggle.com/datasets/felipekitamura/unifesp-xray-bodypart-classification (doi:10.34740/KAGGLE/DSV/3399135) | CC BY-NC-SA 4.0 |
| MURA | Stanford AIMI https://stanford.redivis.com/datasets/cv1a-apytk3j44 | access request + Stanford Dataset Research Use Agreement (non-commercial, **no redistribution**) |
| COVID-19 Radiography Database | https://www.kaggle.com/datasets/tawsifurrahman/covid19-radiography-database | (c) original authors |
| FracAtlas | doi:10.6084/m9.figshare.22363012 | CC BY 4.0 |

**Never commit MURA images, crops or embeddings to this repository.** Details and caveats (Kaggle mirrors, version differences): `docs/DATASET_CHECKS.md`.

## Reproduce
```bash
pip install -r requirements.txt
python -m src.build_index && python -m src.make_splits && python -m src.make_holdout_cv_splits --holdout_fold 4   # inside v2/, UNIFESP_DATA_ROOT set
# training and ensembling: use the notebooks in v2/ (see docs/RUNBOOK.md)
python make_paper_tables.py --root results --out results/paper_tables.md
python make_figures.py
python make_latex.py && python build_docx.py
```
Split fingerprints (SHA-256): `index.csv` 04cc621c95e8a353a665c4a2014b16045a4c6a14af0b944ca9ca9a4ad68a4b8a, `splits/folds.csv` ff44019bf2799d906acbbbe4d8e48f1228f244095a21e768ff9a74a64f36f36a.

## Known limitations
Single-centre data; 323-image held-out set with 1-6 positives for several classes; image-level CIs and splits for the COVID and FracAtlas results; transfer class maps and label-audit suspects not clinician-reviewed; Stage 2 pseudo-labelling uses unlabelled test images (transductive); runs came from several Kaggle accounts; model weights not included; MURA experiments used a third-party Kaggle copy (licence unspecified).

## Licence
Code: MIT. Datasets and derived result files keep their own terms (see `LICENSE`).
