# Decision Mining Summary

## Scope

This intermediate summary documents decision mining on the complete-filtered BPIC-17 event log. The analysis uses branching activities as decision points and predicts the next activity from case attributes and prefix features available before the next step occurs.

## Selected Decision Points

- `A_Validating`: 38,813 instances, 6 target classes after grouping rare successors as `Other`.
- `O_Returned`: 23,303 instances, 6 target classes after grouping rare successors as `Other`.

## Model Metrics


| decision_point | model | accuracy | balanced_accuracy | macro_f1 | weighted_f1 |
| --- | --- | --- | --- | --- | --- |
| A_Validating | DecisionTreeClassifier | 0.5671 | 0.3326 | 0.2674 | 0.5991 |
| A_Validating | RandomForestClassifier | 0.6683 | 0.3816 | 0.3462 | 0.6718 |
| O_Returned | DecisionTreeClassifier | 0.2138 | 0.3911 | 0.2569 | 0.1672 |
| O_Returned | RandomForestClassifier | 0.3543 | 0.4240 | 0.3687 | 0.3646 |

## Interpretation Notes

- The decision trees provide interpretable rules that can be referenced in the report.
- Random forests are used only as a comparison model and for feature importance, not as the main explanatory artifact.
- Class imbalance is present because some successors dominate each decision point.
- Rare successor activities are grouped as `Other`; this improves stability but reduces target granularity.
- Features are restricted to case attributes and prefix information to avoid future leakage.

## Generated Files

- `results/decision_points.csv`
- `results/decision_mining_dataset_overview.csv`
- `results/decision_mining_metrics.csv`
- `results/decision_mining_feature_importance.csv`
- `results/decision_tree_rules.txt`
- `figures/decision_mining/decision_tree_*.pdf/png`
- `figures/decision_mining/confusion_matrix_tree_*.pdf/png`
- `figures/decision_mining/feature_importance_*.pdf/png`