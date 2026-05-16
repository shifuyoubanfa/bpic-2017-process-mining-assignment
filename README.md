# BPIC-2017 Process Mining Assignment

This repository contains reproducible code and intermediate outputs for the
individual assignment in the TUM course **Business Process Prediction,
Simulation and Optimization**. The assignment analyzes the BPIC-17 event log
from a Dutch financial institution's loan application process.

The current project stages are:

1. Simple event log inspection and descriptive analysis.
2. Process discovery and model validation.
3. Decision mining.
4. Advanced analysis with case duration prediction.

The repository does not yet contain the final LaTeX report.

## Dataset

The analysis is based on:

**BPI Challenge 2017**, DOI:
`10.4121/uuid:5f3067df-f10b-45da-b98b-86ae4c7a310b`

The raw BPIC-17 event log is not included in this GitHub repository and should
not be committed. Place the local event log at:

```text
data/BPI Challenge 2017.xes
```

## Environment Setup

Activate the existing Conda environment and install the required packages:

```bash
conda activate process-mining
pip install -r requirements.txt
```

Alternatively, recreate the Conda environment from the project file:

```bash
conda env create -f environment.yml
conda activate process-mining
```

Process model visualization with PM4Py also requires the Graphviz executable
(`dot`) to be available in the active environment. In the local Conda
environment used for this project, this can be installed with:

```bash
conda install -n process-mining graphviz
```

## Run Initial Event Log Inspection

```bash
python src/01_inspect_event_log.py
```

Or run the notebook:

```bash
jupyter notebook notebooks/01_event_log_exploration.ipynb
```

Expected outputs include:

```text
results/basic_log_statistics.csv
results/column_overview.csv
results/top_15_variant_mapping.csv
figures/top_15_activities.*
figures/case_length_distribution.*
figures/case_duration_distribution_days.*
figures/top_15_variants.*
```

## Run Process Discovery and Validation

```bash
jupyter notebook notebooks/02_process_discovery_and_validation.ipynb
```

The notebook first documents lifecycle transitions, then uses
`lifecycle:transition == "complete"` events for process discovery and model
quality evaluation. It attempts full-log evaluation first and records any
fallback to a deterministic sample.

Expected outputs include:

```text
results/lifecycle_transition_distribution.csv
results/event_origin_lifecycle_crosstab.csv
results/process_model_quality.csv
results/process_discovery_parameters.csv
results/process_discovery_summary.md
results/process_models/
figures/process_models/
```

## Run Decision Mining

```bash
jupyter notebook notebooks/03_decision_mining.ipynb
```

The notebook identifies branching activities, selects two interpretable
decision points, and trains shallow decision trees plus random forests using
case attributes and prefix features.

Expected outputs include:

```text
results/decision_points.csv
results/decision_mining_metrics.csv
results/decision_mining_summary.md
results/decision_tree_rules.txt
figures/decision_mining/
```

## Run Advanced Analysis

```bash
jupyter notebook notebooks/04_advanced_case_duration_prediction.ipynb
```

The notebook predicts remaining case duration after the first five complete
events and compares a median baseline against a random forest regressor.

Expected outputs include:

```text
results/advanced_analysis_metrics.csv
results/advanced_analysis_summary.md
results/advanced_analysis_predictions.csv
figures/advanced_analysis/
```

## Final Report

The final TUM-template LaTeX report is in:

```text
report/main.tex
report/main.pdf
```

On this Windows setup, `latexmk` may fail if MiKTeX cannot find Perl. The
repository therefore includes a PowerShell compile helper:

```powershell
powershell -ExecutionPolicy Bypass -File report/compile_report.ps1
```

## Project Structure

```text
.
|-- data/
|   `-- BPI Challenge 2017.xes        # local only, ignored by Git
|-- figures/
|   `-- process_models/
|-- notebooks/
|   |-- 01_event_log_exploration.ipynb
|   |-- 02_process_discovery_and_validation.ipynb
|   |-- 03_decision_mining.ipynb
|   `-- 04_advanced_case_duration_prediction.ipynb
|-- report/
|   |-- main.tex
|   `-- main.pdf
|-- results/
|   `-- process_models/
|-- src/
|   |-- 01_inspect_event_log.py
|   `-- 05_prepare_report_artifacts.py
|-- .gitignore
|-- environment.yml
|-- README.md
`-- requirements.txt
```
