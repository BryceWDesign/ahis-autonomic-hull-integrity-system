"""Mass and energy closure with explicit sinks and bounded residuals."""

from .numeric import scalar


def closure(incoming, terms, *, absolute_tolerance, relative_tolerance):
    incoming = scalar(incoming, lower=0)
    atol = scalar(absolute_tolerance, lower=0)
    rtol = scalar(relative_tolerance, lower=0, upper=1)
    if not terms or any(not isinstance(k, str) or not k.strip() for k in terms):
        raise ValueError("named sinks required")
    values = {k: scalar(v, lower=0) for k, v in terms.items()}
    outgoing = sum(values.values())
    residual = incoming - outgoing
    bound = atol + rtol * incoming
    return {
        "accepted": abs(residual) <= bound,
        "incoming": incoming,
        "terms": values,
        "residual": residual,
        "tolerance": bound,
        "scope": "CONSERVATION_ACCOUNTING__NOT_A_PERFORMANCE_PREDICTION",
    }


def impact_energy(mass_kg, speed_m_s, terms_j, **tolerances):
    m = scalar(mass_kg, lower=0)
    v = scalar(speed_m_s, lower=0)
    return closure(0.5 * m * v * v, terms_j, **tolerances)


def agent_mass(initial_g, delivered_g, remaining_g, measured_loss_g, **tolerances):
    return closure(
        initial_g,
        {"delivered_g": delivered_g, "remaining_g": remaining_g, "measured_loss_g": measured_loss_g},
        **tolerances,
    )
