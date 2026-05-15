# Process Discovery and Validation Summary

## Scope

This intermediate summary documents process discovery and model validation for the BPIC-17 event log. It compares Inductive Miner, Heuristics Miner, Alpha Miner, and a directly-follows graph using a complete-event representation of the log.

## Preprocessing

The raw log contains 1,202,267 events and 31,509 cases. After filtering to `lifecycle:transition == complete`, the discovery log contains 475,306 events and 31,509 cases.

Only complete events are used because they represent the completion of business activities and reduce noise from task lifecycle states such as schedule, start, suspend, and resume. The risk is that start, schedule, withdraw, suspend, and resume information may be lost. The original lifecycle distribution and EventOrigin-lifecycle crosstab are therefore saved separately.

## Quality Metrics

| algorithm | status | discovery_scope | evaluation_scope | used_fallback | fitness | fitness_scope | precision | precision_scope | generalization | generalization_scope | built_in_simplicity | number_of_places | number_of_transitions | number_of_arcs | average_arc_degree | silent_transition_ratio | error_note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Inductive Miner | success | complete_filtered_full_log | complete_filtered_full_log | False | 1.0 | complete_filtered_full_log | 0.2926135820916598 | complete_filtered_full_log | 0.9756702764431168 | complete_filtered_full_log | 0.6170212765957447 | 34 | 53 | 114 | 1.3103448275862069 | 0.5471698113207547 |  |
| Heuristics Miner | success | complete_filtered_full_log | complete_filtered_full_log | False | 0.8340345865584254 | complete_filtered_full_log | 0.9979262430596038 | complete_filtered_full_log | 0.8475042684572474 | complete_filtered_full_log | 0.48148148148148145 | 49 | 94 | 220 | 1.5384615384615385 | 0.7446808510638298 |  |
| Alpha Miner | success | complete_filtered_full_log | complete_filtered_full_log | False | 0.495774473479623 | complete_filtered_full_log | 0.12590195124851544 | complete_filtered_full_log | 0.9869939686795314 | complete_filtered_full_log | 0.392 | 25 | 24 | 87 | 1.7755102040816326 | 0.0 |  |

## Fallback Notes

- No discovery or metric fallback was needed; all evaluated metrics used the complete-filtered full log.

## Generated Files

- `results/lifecycle_transition_distribution.csv`
- `results/event_origin_lifecycle_crosstab.csv`
- `results/process_model_quality.csv`
- `results/process_discovery_parameters.csv`
- `results/process_discovery_summary.md`
- `results/process_models/inductive_miner.pnml`
- `results/process_models/heuristics_miner.pnml`
- `results/process_models/alpha_miner.pnml`
- `results/process_models/inductive_miner.bpmn`
- `figures/process_models/inductive_miner_petri_net.pdf`
- `figures/process_models/inductive_miner_process_tree.pdf`
- `figures/process_models/inductive_miner_bpmn.pdf`
- `figures/process_models/heuristics_miner_petri_net.pdf`
- `figures/process_models/alpha_miner_petri_net.pdf`
- `figures/process_models/dfg_top_edges.pdf`

## Interpretation Notes for Report

- Inductive Miner is the primary structured model candidate.
- Heuristics Miner provides a frequency-aware comparison model for noisy behavior.
- Alpha Miner is treated as a baseline and may perform worse on real-life noisy logs.
- DFG is useful for explaining high-frequency directly-follows relations, but it is not a full behavioral model for conformance checking.
- Fitness, precision, generalization, and simplicity should be interpreted jointly rather than as a single ranking.