# Requirement Completion Checklist

This file tracks whether the repository contains material for each required part
of the assignment. It is an intermediate planning and verification artifact, not
the final report.

| Required part | Status | Main material |
|---|---|---|
| Technical setup and preliminaries | Prepared | `README.md`, `requirements.txt`, `environment.yml`, `.gitignore` |
| Simple event log analysis | Prepared | `notebooks/01_event_log_exploration.ipynb`, `results/simple_event_log_analysis_summary.md`, descriptive figures |
| Process model creation and validation | Prepared | `notebooks/02_process_discovery_and_validation.ipynb`, `results/process_model_quality.csv`, model figures and PNML/BPMN exports |
| Decision mining | Prepared | `notebooks/03_decision_mining.ipynb`, `results/decision_mining_summary.md`, decision tree and confusion matrix figures |
| One advanced analysis | Prepared | `notebooks/04_advanced_case_duration_prediction.ipynb`, `results/advanced_analysis_summary.md`, duration prediction metrics and figures |
| Final LaTeX report | Not started by design | To be created after user acceptance of analysis materials |

## Notes For Report Writing

- The final report can now be written from prepared intermediate materials.
- Decision mining results should be interpreted cautiously because branch targets
  are imbalanced and rare successors are grouped as `Other`.
- Advanced duration prediction improves only modestly over the median baseline,
  which is itself an important finding about early-case predictability.
- The raw BPIC-17 XES log remains local and must not be committed.
