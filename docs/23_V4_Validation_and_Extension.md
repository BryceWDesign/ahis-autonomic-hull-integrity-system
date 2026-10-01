# Validation and extending the reference model

The release gate is `python check_green.py`. It covers the entire inherited test suite, v4 tests, the retained v3 deterministic campaign, fresh v4 campaign, archived v4 replay, source/claim boundaries, v4 lint and formatting, P1 build/CAD package and full-tree SHA-256 integrity.

The v4 campaign contains 31 cases. Acceptance means the expected decision happened, including expected rejections. It does not mean all requested repairs succeeded. The nominal, alternative-isolation and held-out weak-response cases recover only to RECOVERED_LIMITED. The remaining cases isolate. Tampered and rehashed-tampered evidence must fail audit.

The suite includes analytic leak-volume comparison, orthogonal SVD reconstruction, independently computed information-determinant gain, isotropic arrival-gradient comparison, zero-authority rejection, full local authority with infeasible resource bounds, exact lock rejection, fixed-command uncertainty failure, held-out limit enforcement, failed-verification consumption, measured-loss subtraction and physical-credit firewall tests.

## To extend beyond the four-coordinate synthetic experiment

1. Define measured state coordinates, units, normalization and an experiment-specific two-sided survival policy.
2. Measure actuator influence maps and nonlinear responses for the actual article. Archive calibrations, validity ranges and uncertainties.
3. Define resource demand using measured flows, energy and cycle lifetimes. Include thermal and electrical coupling explicitly.
4. Substitute calibrated response and constraints in `InfluenceBasis` and update the reference coordinate/unit guards in `controller.py`. The generic SVD, conservation, sensing and state libraries remain reusable.
5. Establish independent held-out channels and trustworthy acquisition groups. Archive actual measurements and commands.
6. Calibrate any propagation graph delays, or replace the graph with validated physical solvers and independent tests.
7. Run the complete tests and failure campaign. Regenerate source-bound evidence and manifest only after review of intended changes.
8. Perform the separate physical validation/promotion procedure. Software gates never update `PHYSICAL_STATUS.json` to true.

Existing v3 digital-twin discrepancy and remaining-life screens remain available and tested; v4 does not invent a new qualified fatigue model or combine those screens into a physical life certification.
