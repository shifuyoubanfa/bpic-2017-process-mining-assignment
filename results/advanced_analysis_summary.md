# Advanced Analysis Summary: Case Duration Prediction

## Scope

This advanced analysis predicts remaining case duration after the first 5 complete events of a case. The task uses only case attributes and prefix-level behavior observed before the prediction point.

## Dataset

- Eligible cases: 31,509
- Train cases: 22,056
- Test cases: 9,453
- Target: `remaining_duration_days`

## Model Metrics

| model | mae_days | rmse_days | r2 | train_cases | test_cases |
| --- | --- | --- | --- | --- | --- |
| MedianBaseline | 10.1304 | 12.7735 | -0.0787 | 22056 | 9453 |
| RandomForestRegressor | 9.9492 | 12.1153 | 0.0296 | 22056 | 9453 |

## Interpretation Notes

- The median baseline is included to show whether the machine-learning model adds predictive value.
- The random forest captures non-linear relationships in early case behavior but is less interpretable than a shallow tree.
- The target is remaining duration after a fixed prefix, so it avoids using future events as features.
- Errors may be larger for unusually long-running cases, which should be discussed as a limitation.

## Generated Files

- `results/advanced_duration_prediction_dataset_overview.csv`
- `results/advanced_analysis_metrics.csv`
- `results/advanced_analysis_predictions.csv`
- `results/advanced_analysis_feature_importance.csv`
- `figures/advanced_analysis/predicted_vs_actual_duration.pdf/png`
- `figures/advanced_analysis/error_distribution.pdf/png`
- `figures/advanced_analysis/feature_importance.pdf/png`