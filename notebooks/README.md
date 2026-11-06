# Notebooks (reusable)
All notebooks run on Kaggle (GPU T4 x2 where noted) and **do not need local data**: attach the dataset named in the first markdown cell (Notebook Settings -> Data) and press Run All.

## `ready_to_run/` -- final notebooks of the paper (generated from `../v2/src` by `v2/build_*.py`)
| Notebook | Needs (Kaggle inputs) | Purpose |
|---|---|---|
| `UNIFESP_v2_stage2_boost.ipynb` | UNIFESP dataset | Stage 2: 16-model ensemble, pseudo-labels (about 5.2 h on 2 x T4) |
| `UNIFESP_v2_reliability.ipynb` | UNIFESP + output of the ablation-suite notebook (`runs/*/preds.npz`), CPU | calibration, selective prediction, per-class CIs, label audit |
| `UNIFESP_v2_fm_probe.ipynb` | UNIFESP, internet on | frozen DINOv2 / Swin linear probe, label-efficiency curve |
| `UNIFESP_v2_mura.ipynb` | MURA copy (see `docs/DATASET_CHECKS.md` for access terms) | MURA body-part benchmark (official split) |
| `UNIFESP_v2_covid.ipynb` | `tawsifurrahman/covid19-radiography-database` | COVID-19 Radiography (image-level split) |
| `UNIFESP_v2_cross.ipynb`, `UNIFESP_v2_cross_fracatlas.ipynb` | UNIFESP, MURA, FracAtlas, weights of earlier runs | zero-shot transfer through the class map |
| `UNIFESP_v2_explain.ipynb` | UNIFESP + trained weights | Grad-CAM, faithfulness and randomisation checks |
The ablation-suite notebook is `../v2/UNIFESP_v2_ablation.ipynb` (and `UNIFESP_v2_pipeline.ipynb` / part1of2 / part2of2).

## `earlier/` -- earlier exploratory notebooks (kept for provenance; superseded by the notebooks above)
They contain the older, partly leaky evaluation (thresholds/checkpoints chosen on the scored fold). Do not quote their numbers except in the leakage comparison.

## Rules
* Never put MURA images in the repository or in a public Kaggle dataset (Stanford research agreement).
* After a run, copy the printed output into `results/` and regenerate tables with `make_paper_tables.py`.
