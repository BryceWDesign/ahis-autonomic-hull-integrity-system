# Software proof of concept

The proof is a manufactured four-coordinate damaged-article scenario. Planning evidence, response gains, acquisition groups, graph delays and material-screen inputs are explicitly synthetic. It exercises the coordinated architecture and its failure gates.

Open `results/v4_survival_campaign/nominal.json`. Its request archives the raw channels, arrivals, calibration IDs, policy, resources and uncertainty cases. Its result shows preservation, containment, planned paired-agent/damping/heater actions, held-out checks and RECOVERED_LIMITED. Its physical and hardware authority flags remain false.

Compare `seal_actuator_lost.json` and `isolation_substitutes_for_seal.json`. Without sealing authority the original action set cannot meet the envelope. When the separate synthetic isolation coordinate is available, the optimizer can choose a different feasible response. This is a software control demonstration, not measured sealing/valve capability.

Compare `no_safe_heater.json`, `exact_lock_blocks_repair.json`, `agent_depleted.json` and `robustness_failure.json`. The controller isolates rather than treating an unconstrained inverse or nominal prediction as an authorized plan.

Compare `heldout_failed.json`, `heldout_reuses_acquisition_group.json`, `mass_nonclosure.json`, `executed_command_mismatch.json` and `resource_overdraw.json`. A successful numerical proposal does not suffice for limited recovery. Required independent response evidence, command consistency and conservation must all pass.

Run `python check_green.py` to reproduce the campaigns and audit every archived decision. The independent analytic/unit checks are in `tests/test_survival_math_v4.py`; the end-to-end adverse cases and evidence tests are in `tests/test_survival_assurance_v4.py`.
