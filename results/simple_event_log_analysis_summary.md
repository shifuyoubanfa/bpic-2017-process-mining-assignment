# Simple Event Log Analysis Summary

## Scope

This summary is an intermediate note for the BPIC-17 simple event log analysis. It describes the inspected XES event log, the basic case/event statistics, activity and variant distributions, and two additional descriptive distributions: `EventOrigin` and `case:LoanGoal`.

## Key Statistics

| Metric | Value |
|---|---:|
| Number of events | 1,202,267 |
| Number of cases | 31,509 |
| Number of unique activities | 26 |
| Number of resources | 149 |
| Number of process variants | 15,930 |
| Number of case attribute columns | 3 |
| Number of event attribute columns | 15 |
| Number of categorical event attributes | 9 |
| Mean case length | 38.16 events |
| Std case length | 16.72 events |
| Min case length | 10 events |
| Median case length | 35 events |
| Max case length | 180 events |
| Mean case duration | 21.90 days |
| Std case duration | 13.17 days |
| Min case duration | 0.0023 days |
| Median case duration | 19.09 days |
| Max case duration | 286.07 days |

## Interpretation

The BPIC-17 event log is large enough to support meaningful process mining analysis, with more than 1.2 million events across 31,509 cases. The log contains 26 distinct activities and 149 resources. The 15,930 observed process variants indicate substantial behavioral diversity, which is important context for interpreting the simple event log analysis.

Case lengths are moderately dispersed around an average of 38.16 events, with a maximum of 180 events. Case durations show a mean throughput time of about 21.90 days and a much larger maximum of about 286.07 days, suggesting that some cases stay open far longer than typical cases. Workflow events dominate the log by event count, followed by application and offer events. The most common loan goals are `Car`, `Home improvement`, and `Existing loan takeover`.

## Generated Figures

| Figure | Description |
|---|---|
| `figures/top_15_activities.png` / `.pdf` | Top 15 activity frequencies |
| `figures/case_length_distribution.png` / `.pdf` | Distribution of events per case |
| `figures/case_duration_distribution_days.png` / `.pdf` | Distribution of case durations in days |
| `figures/top_15_variants.png` / `.pdf` | Top 15 process variants using short variant labels |
| `figures/event_origin_distribution.png` / `.pdf` | Distribution of event origins |
| `figures/loan_goal_distribution.png` / `.pdf` | Distribution of loan goals by case |

## Generated Result Files

| Result file | Description |
|---|---|
| `results/basic_log_statistics.csv` | Basic event log, case length, duration, and variant statistics |
| `results/column_overview.csv` | Column names, dtypes, missing values, missing ratios, and unique values |
| `results/top_15_variant_mapping.csv` | Mapping from short variant labels to full activity sequences |
| `results/event_origin_distribution.csv` | Event counts by `EventOrigin` |
| `results/loan_goal_distribution.csv` | Case counts by `case:LoanGoal` |
| `results/simple_event_log_analysis_summary.md` | Intermediate summary for later report writing |
