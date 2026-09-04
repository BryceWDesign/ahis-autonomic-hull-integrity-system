# Multimodal SHM and Localization

## Fusion
`src/ahis/fusion.py` combines bounded damage scores with explicit quality weights. It preserves disagreement as an output and penalizes confidence when modalities disagree. This is intentionally transparent; no trained model is granted operational authority without a real independently validated dataset.

## Anisotropic localization
`src/ahis/localization_v3.py` replaces scalar-wave-speed-only logic with a directional propagation model. The model supports a principal material axis and bounded anisotropy fraction. The grid search estimates source time and reports a near-optimal confidence radius.

The model is still a research approximation. Real composite panels require calibration for anisotropy, dispersion, geometry, boundary reflections, temperature and sensor coupling. The v3 API therefore exposes those assumptions rather than hiding them.

## Sensor-health rule
Low-quality or failed channels reduce effective evidence weight. If quality quorum drops below the configured threshold, the algorithm returns `accepted=False` instead of inventing a location.
