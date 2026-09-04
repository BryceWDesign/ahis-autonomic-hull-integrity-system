# Claim Boundary

## What a GREEN v3 repository means
A GREEN repository means the shipped software compiles, its automated tests pass, the deterministic software/HIL campaign passes, the explicit license/status artifacts are internally consistent, and the release manifest verifies.

## What GREEN does not mean
GREEN does **not** mean:
- a hull survived pressure;
- a structural crack healed;
- a repaired laminate recovered certified strength;
- an ionomer sealed a puncture;
- a vitrimer restored fracture toughness;
- an SMA/MMC article repaired itself;
- a vessel is safe for people;
- a design is flight-, marine-, defense-, industrial-, or life-support-qualified.

`PHYSICAL_STATUS.json` is the machine-readable boundary. The release gate requires every physical claim to remain false unless a later human-reviewed release deliberately changes it after real evidence exists.

## P1 claim
A successful P1 campaign would support only this bounded statement:

> Under the specified gravity-head bench conditions, the P1 autonomous system detected a leak condition, commanded its two-agent research sealing surrogate, and reduced measured leak rate by the stated amount in at least two of three independent runs.

It would still grant **zero structural-strength and hull-survivability credit**.
