# Mathematics and reference-model limits

## Local authority

With state residual r, influence Jacobian J and positive scales s, the diagnostic decomposes r/s into its projection on the columns of J/s and an orthogonal remainder. Exact protected-action rows C define a safe basis Z spanning ker(C); the diagnostic then uses (J/s)Z. Rank is determined by singular values relative to the largest singular value. The reported unreachable fraction is the norm of the orthogonal remainder divided by the norm of the scaled residual.

The implementation uses established SVD mathematics. It does not claim to invent controllability, null spaces, optimization or D-optimal design. The integrated diagnostic selects the currently violated objectives and removes commands with zero remaining bounds before decomposition. Coordinates already inside their intervals remain protected by the nonlinear two-sided optimizer checks; they are not artificially treated as exact no-change targets. Saturation and resource depletion are assessed separately.

## Nonlinear reference response

Native commands are paired repair volume in mL per reservoir, damping-ratio increment, heater fraction and isolation fraction. The last two are synthetic research coordinates. A paired volume consumes the same requested volume from both reservoirs and two pump cycles.

The leak response calls `HILRig.frame`, including its existing minimum leak-ratio floor of 0.02. For equal paired volume v before that floor is reached, leak ratio is exp(-v/8). An independent analytic test checks the nominal 80% reduction target at -8 ln(0.2), approximately 12.8755 mL per reservoir. This is a synthetic-model equality, not a physical recipe recommendation or measured material saving.

The damping response uses AHIS's base-excited SDOF resonant-transmissibility function. The heater coordinate reduces synthetic strain ratio by 0.6 per unit and raises temperature by 30 degrees C per unit; damping adds 8 degrees C per unit. Isolation multiplies leak by (1 - 0.9u). These coefficients are manufactured to exercise joint constraints. They have no physical calibration or protection credit.

## Planning

SLSQP minimizes a strictly positive weighted action cost subject to nonnegative command bounds, the declared resource matrix, two-sided survival bounds in every finite uncertainty case, and optional C u = 0 constraints. Action coordinates are scaled by their upper bounds. The solution is local; no global minimum is claimed. Solver failure, violated constraints, missing authority or cycle exhaustion yields a zero authorized proposal.

The reference uncertainty set includes nominal, weakened response and hotter response. Commands stay fixed for all evaluations. The independent post-solve checker uses the original bounds, with scaled numerical tolerance. The solver uses a small interior margin. Gains and state biases are declared inputs, not probability distributions.

## Active sensing

The travel-time gradient is computed from the retained anisotropic propagation model. The event time is estimated as a nuisance parameter. The information matrix includes a declared positive-definite prior and the surviving arrival gradients weighted by timing variance. Candidate gain is log(1 + a^T I^-1 a / sigma^2). Hardware absence, failed health or reuse excludes a candidate. This is an advisory among already declared channels, not a command to install a sensor.

## Other screens

Propagation is shortest-time directed reachability in a supplied graph, not crack mechanics, CFD, load redistribution FEA or thermal diffusion. Energy and mass closure verify accounting supplied in a record; they do not validate how a material dissipated energy. Layer mass sums density times thickness. Geometry ranking uses supplied mass, stiffness and utility values. The reversible phase is a bounded exponential relaxation with separate on/off thresholds; it is not a constitutive CAHS, polymer or impact model.

## Technical sources

- NumPy SVD documentation: https://numpy.org/doc/stable/reference/generated/numpy.linalg.svd.html
- SciPy SLSQP documentation: https://docs.scipy.org/doc/scipy/reference/optimize.minimize-slsqp.html
- NASA shield-development background: https://hvit.jsc.nasa.gov/shield-development/

These references support methods or research context. They provide no validation of AHIS materials or hardware.
