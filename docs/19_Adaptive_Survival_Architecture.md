# Adaptive Survival Envelope, v4

AHIS v4 adds an executable survivability research path above the retained v3 platform. Its reference experiment is synthetic/HIL. It is neither a qualified hull controller nor an actuator dispatcher.

The decision path is raw planning measurements and acoustic arrivals → localization and fusion → preservation → confirmed containment → local authority assessment → bounded joint planning across the finite uncertainty set → archived response and resource measurements → held-out verification → limited recovery or isolation. There is no automatic operational requalification.

## Implemented boundaries

| Component | Implementation | Meaning |
|---|---|---|
| Survival policy | `survival/survival_envelope.py` | Two-sided limits with explicit units and normalization |
| Influence basis | `survival/influence_basis.py` | Four synthetic action coordinates; leak and modal response call retained AHIS models |
| Local authority | `survival/controllability.py` | Scaled SVD projection and exact-protection null-space diagnostic |
| Joint plan | `survival/survival_optimizer.py` | SLSQP, action/resource bounds, exact locks, independent feasibility checks |
| Robustness | `survival/uncertainty.py` | Same command evaluated in every declared case; no reoptimization per case |
| State policy | `survival/adaptive_state.py` | Explicit preservation, containment, repair, verification, limited-recovery and isolation transitions |
| Active sensing | `survival/active_sensing.py` | Anisotropic arrival Jacobians, event-time nuisance parameter, surviving-channel information gain |
| Propagation | `survival/propagation.py` | Graph reachability with declared delays and closed barriers |
| Conservation | `survival/accounting.py` | Explicit mass/electrical/impact-energy sinks and residual tolerances |
| Held-out checks | `survival/independent_verify.py` | Distinct sensor IDs and acquisition groups; required channels and quorum |
| Integration | `survival/controller.py` | Recomputes the entire path from archived inputs |
| Replay | `survival/replay_audit.py` | Input/source binding, exact integrity, numerical recomputation, external trusted digest option |
| Protection screens | `survival/protection_stack.py` | Layer mass, hysteretic phase and supplied geometry-candidate ranking |
| Research gates | `survival/research_programs.py` | Program-specific record completeness, human-review eligibility only |

All paths above are under `src/ahis/`. The implementation consolidates related functions rather than creating empty modules for every proposed filename.

The v3 P1 serial controller is retained as a separate physical reference-article path. The new four-action basis is not wired to P1, heating hardware, a hull, a piezoelectric mesh, or isolation valves. This separation avoids silently giving a synthetic response model hardware authority.

## Control versus physical support

The first two influence coordinates reuse AHIS's synthetic leak and modal functions. Heater/strain and isolation effects are declared toy coefficients. State scales are experiment policy, not structural allowables. Calibrated measured influence maps, sensor covariance, actuator dynamics and qualified process windows are required before any hardware adaptation.

A nonzero unreachable fraction is a local tangent-space diagnostic. A zero fraction does not prove global recovery. The optimizer performs the nonlinear bounded checks separately. Likewise, finite uncertainty cases prove behavior only for that declared set, not arbitrary uncertainty or a certified probability of survival.

There is no hard real-time timing guarantee, material finite-element model, calibrated fracture/thermal-flow solver, flight software certification, or full-scale structural qualification.
