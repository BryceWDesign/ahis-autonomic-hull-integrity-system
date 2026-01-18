# Contributing to AHIS

AHIS is an engineering proof-of-concept (PoC) repository focused on **measurable, testable** hull protection concepts. Contributions are welcome if they improve scientific clarity, verification quality, or implementation rigor.

## Core contribution rules (non-negotiable)
1) **No unmeasurable claims.**  
   Any performance statement must include: a metric, units, a test method, and acceptance criteria.
2) **No “crew-safe / flight-ready” language.**  
   This repo is PoC. Safety claims require independent validation outside this repository.
3) **No nonstandard physics framing.**  
   Avoid terms like “nullification,” “Tesla 3-6-9,” “field cancellation,” etc. Use standard language: SHM, modal analysis, FRF, impedance/admittance, guided waves, damping ratio, transmissibility.
4) **No hidden assumptions.**  
   If you assume environment, boundary conditions, material properties, or sensor placement—state it explicitly.

## What to contribute
Good contributions include:
- Clarifying architecture and subsystem interfaces
- Improving requirements and acceptance criteria
- Adding or refining test protocols (with instrumentation requirements and pass/fail thresholds)
- Adding analysis scripts that produce repeatable outputs (plots/tables) from provided data templates
- Tightening definitions, terminology, and failure-mode documentation (FMEA-lite)

Avoid:
- “Marketing” language or speculative promises
- Large refactors that reduce traceability to legacy sources without providing a mapping

## Contribution format standards
### Documentation
- Use plain Markdown (`.md`).
- Keep statements falsifiable.
- Every doc that asserts a mechanism should include:
  - **Inputs**
  - **Outputs**
  - **Assumptions**
  - **Failure modes**
  - **Verification method**

### Code / scripts
- Prefer readability over cleverness.
- Include:
  - minimal dependencies
  - clear argument handling
  - deterministic outputs where possible
  - comments explaining units and assumptions
- Do not include API keys, tokens, or secrets.

### Data and results
- Do not fabricate results.
- If data is simulated, label it **SIMULATED** and include the model assumptions.
- Use the repository’s results template when adding any “result package.”

## Review criteria (what maintainers will check)
- Scientific correctness and standard terminology
- Traceability: can a reviewer see where a concept came from and what changed?
- Verification readiness: does the change improve testability or interpretability?
- Risk transparency: are new risks documented?

## License and permission
By submitting contributions, you agree your changes may be incorporated under the repository’s licensing terms. If you cannot accept that, do not submit a contribution.

## Reporting security issues
See `SECURITY.md`. Do not open public issues for vulnerabilities.

---
Maintainer: Bryce Lovell
