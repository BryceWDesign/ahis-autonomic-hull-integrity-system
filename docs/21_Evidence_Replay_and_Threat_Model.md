# Evidence, replay and trust

Each v4 bundle contains the complete raw request, declared synthetic calibration identities, policy/model/resource inputs, software-file hashes, dependency versions, reconstructed decision, state transitions and hash-chained history. The outer SHA-256 digest covers all fields other than the digest itself.

`ahis audit bundle.json` checks exact bundle integrity and source identity, then reruns localization, fusion, authority assessment, sensing advice, propagation, joint optimization, resource checks, conservation, held-out verification and state policy. Rehashing an altered verdict does not make recomputation pass. Tests also cover source substitution and external trusted-digest mismatch.

Floating-point scientific values use absolute tolerance 1e-7 plus relative tolerance 1e-6. Structural fields, booleans, keys and source hashes are strict. Dependency differences are reported. Solver iteration counts/messages are archived diagnostics but are excluded from authoritative replay equivalence because local numerical solvers may reach the same accepted decision in a different number of iterations or with platform-specific diagnostic text. SHA-256 checks are exact, even when numerical replay uses tolerance.

A hash chain is not a signature. A party who replaces the entire request, result, software and digest can create a new internally consistent bundle. An externally retained digest, trustworthy acquisition chain and human review remain necessary. `--trusted-digest` binds audit to an externally retained value. This release does not implement signing, key custody, remote attestation or trusted physical acquisition.

## Independent verification

The reference path requires four held-out coordinates in the declared order and units, each with exactly the survival-policy interval and `required: true`. IDs and acquisition groups must be distinct from the planning channels, arrival bus and fusion bus. At least two independent groups are required, and every required channel must be healthy and pass. A caller cannot relax the held-out limits while preserving the original policy.

For an accepted executed command, AHIS predicts the complete post-response vector for every declared finite uncertainty scenario. Each healthy held-out value must remain inside both the survival-policy envelope and the per-coordinate executed-command bounds. In addition, the complete held-out response vector must be coherent with at least one complete declared scenario prediction. A value that is outside the executed-command bounds is rejected as `RESPONSE_MODEL_INCONSISTENT`; a vector assembled from individually plausible coordinates that cannot occur together in any declared scenario is rejected as `RESPONSE_SCENARIO_INCONSISTENT`. The comparison includes only numerical tolerance; no physically calibrated sensor-noise allowance or continuous uncertainty interpolation is claimed.

IDs/groups are archived declarations. Software cannot prove that two allegedly independent channels are physically independent, correctly calibrated, or free from common-mode failure. The synthetic campaign uses the same surrogate family to manufacture held-out observations, with separate weak-response and failure controls. It does not claim independent physical validation.

## Resource evidence

Archived executed commands must match the recomputed plan. Measured delivered mass/electrical consumption must match the declared consumption vector. Initial ledger inventory must match the available inventory. Delivered/consumed, remaining and measured-loss terms must close. The next inventory subtracts both measured consumption and loss. Post-response verification failure retains that consumption; a denied proposal does not reserve or consume resources. Invalid accounting marks inventory unverified and prevents limited-recovery acceptance.

All v4 results retain `physical_credit: false`, `hardware_authority: false`, `return_to_service_allowed: false` and `next_repair_allowed: false`. P1 physical evidence remains separately governed by its inherited controller and assessment tools.
