from copy import deepcopy
import math
import numpy as np
import pytest
from ahis.survival.numeric import finite, scalar, load_json
from ahis.survival.controllability import decompose, safe_modes
from ahis.survival.survival_envelope import Envelope
from ahis.survival.influence_basis import InfluenceBasis
from ahis.survival.survival_optimizer import solve
from ahis.survival.uncertainty import campaign
from ahis.survival.active_sensing import advise, arrival_jacobian
from ahis.localization_v3 import AnisotropicPropagation
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def config():
    return load_json(ROOT / "configs/survival_reference.json")


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), -float("inf")])
def test_nonfinite_array_rejected(bad):
    with pytest.raises(ValueError):
        finite([1, bad])


@pytest.mark.parametrize("bad", [True, "1", None, float("nan"), float("inf")])
def test_invalid_scalar_rejected(bad):
    with pytest.raises(ValueError):
        scalar(bad)


def test_two_objectives_are_locally_controllable():
    r = decompose(np.eye(2), [1, 1], scales=[1, 1])
    assert r["rank"] == 2 and r["unreachable_fraction"] < 1e-12


@pytest.mark.parametrize("missing", [0, 1])
def test_lost_authority_detects_unreachable_component(missing):
    j = np.eye(2)
    j[:, missing] = 0
    r = decompose(j, [1, 1], scales=[1, 1])
    assert r["rank"] == 1
    assert r["unreachable_fraction"] == pytest.approx(1 / math.sqrt(2))


def test_unit_scaling_changes_interpretation_without_hiding_unreachable_mode():
    r = decompose([[1], [0]], [1000, 2], scales=[1000, 2])
    assert r["unreachable_fraction"] == pytest.approx(1 / math.sqrt(2))


def test_exact_protection_can_remove_every_safe_action():
    z, rank = safe_modes(np.eye(3), 3)
    assert z.shape == (3, 0) and rank == 3
    r = decompose(np.eye(3), [1, 1, 1], scales=[1, 1, 1], protected=np.eye(3))
    assert r["unreachable_fraction"] == pytest.approx(1)


def test_rank_deficient_svd_reconstruction_is_orthogonal():
    j = np.array([[1, 2], [2, 4], [0, 0]])
    r = decompose(j, [2, 1, 3], scales=[1, 1, 1])
    a = np.array(r["reachable_scaled"])
    b = np.array(r["unreachable_scaled"])
    assert np.allclose(a + b, [2, 1, 3]) and abs(a @ b) < 1e-12


@pytest.mark.parametrize("scale", [[0, 1], [-1, 1], [1], [1, float("nan")]])
def test_invalid_authority_scales_fail(scale):
    with pytest.raises(ValueError):
        decompose(np.eye(2), [1, 1], scales=scale)


def test_resource_minimum_matches_independent_analytic_leak_solution(config):
    c = deepcopy(config)
    c["basis"]["state"][3] = 0.6
    c["envelope"]["upper"][1] = 1.01
    c["basis"]["available"] = [True, False, False, False]
    b = InfluenceBasis(c["basis"])
    e = Envelope.from_dict(c["envelope"])
    plan = solve(b, e, [50, 50, 500], [{"id": "nominal", "gain": [1] * 4, "bias": [0] * 4}], margin=0)
    assert plan["accepted"]
    expected = -8 * math.log(0.2)
    assert plan["proposal"][0] == pytest.approx(expected, rel=1e-6)
    assert plan["resource_demand"][:2] == pytest.approx([expected, expected])


def test_full_rank_does_not_imply_bounded_feasibility(config):
    b = InfluenceBasis(config["basis"])
    e = Envelope.from_dict(config["envelope"])
    local = decompose(b.jacobian()[:2], np.maximum(b.state[:2] - e.upper[:2], 0), scales=e.scales[:2])
    assert local["unreachable_fraction"] < 1e-5
    plan = solve(b, e, [1, 1, 1], config["uncertainty"])
    assert not plan["accepted"] and plan["authorized_command"] == [0] * 4


def test_solver_command_is_frozen_across_uncertainty_cases(config):
    b = InfluenceBasis(config["basis"])
    e = Envelope.from_dict(config["envelope"])
    p = solve(b, e, config["budget"]["resources"], config["uncertainty"])
    assert p["accepted"] and p["robustness"]["all_pass"]
    rows = config["uncertainty"] + [{"id": "extreme", "gain": [0.2] * 4, "bias": [0] * 4}]
    q = campaign(b, e, p["proposal"], rows)
    assert not q["all_pass"] and q["fixed_command"] == p["proposal"]


def test_zero_surviving_actions_fails_without_resource_consumption(config):
    config["basis"]["available"] = [False] * 4
    p = solve(
        InfluenceBasis(config["basis"]),
        Envelope.from_dict(config["envelope"]),
        [50, 50, 500],
        config["uncertainty"],
    )
    assert not p["accepted"] and p["authorized_command"] == [0] * 4
    assert p["resource_remaining"] == [50, 50, 500]


def test_exact_lock_suppresses_heater_and_blocks_required_strain_recovery(config):
    p = solve(
        InfluenceBasis(config["basis"]),
        Envelope.from_dict(config["envelope"]),
        [50, 50, 500],
        config["uncertainty"],
        protected=[[0, 0, 1, 0]],
    )
    assert not p["accepted"] and p["authorized_command"] == [0] * 4


@pytest.mark.parametrize(
    "change", ["physical", "negative_cost", "bad_dimensions", "negative_resources", "bad_zeta"]
)
def test_invalid_basis_rejected(config, change):
    d = config["basis"]
    if change == "physical":
        d["evidence_class"] = "PHYSICAL"
    elif change == "negative_cost":
        d["cost"][0] = -1
    elif change == "bad_dimensions":
        d["upper"] = [1]
    elif change == "negative_resources":
        d["resource_matrix"][0][0] = -1
    else:
        d["baseline_zeta"] = 2
    with pytest.raises(ValueError):
        InfluenceBasis(d)


def test_d_optimal_advice_matches_information_determinant():
    info = np.diag([2.0, 3.0])
    a = np.array([1.0, 2.0])
    rows = [
        {"id": "good", "healthy": True, "hardware_present": True, "noise_std": 0.5, "jacobian": a},
        {"id": "weak", "healthy": True, "hardware_present": True, "noise_std": 0.5, "jacobian": [0, 0]},
    ]
    r = advise(info, rows)
    assert r["recommended"] == "good"
    expected = np.linalg.det(info) / np.linalg.det(info + np.outer(a, a) / 0.25)
    assert r["ranking"][0]["covariance_determinant_ratio"] == pytest.approx(expected)


@pytest.mark.parametrize("field", ["healthy", "hardware_present"])
def test_failed_or_nonexistent_sensor_not_recommended(field):
    row = {"id": "S1", "healthy": True, "hardware_present": True, "noise_std": 1.0, "jacobian": [1, 1]}
    row[field] = False
    assert advise(np.eye(2), [row])["recommended"] is None


def test_used_sensor_is_not_new_information_candidate():
    row = {"id": "S1", "healthy": True, "hardware_present": True, "noise_std": 1.0, "jacobian": [1, 1]}
    assert advise(np.eye(2), [row], used_ids=["S1"])["recommended"] is None


@pytest.mark.parametrize("info", [[[1, 2], [0, 1]], [[0, 0], [0, 0]], [[-1, 0], [0, 1]]])
def test_invalid_prior_information_rejected(info):
    with pytest.raises(ValueError):
        advise(info, [])


def test_arrival_jacobian_matches_isotropic_analytic_derivative():
    p = np.array([0.3, 0.4])
    s = np.array([0.0, 0.0])
    v = 2500.0
    j = arrival_jacobian(p, s, AnisotropicPropagation(v))
    assert j == pytest.approx([0.3 / (0.5 * v), 0.4 / (0.5 * v), 1.0], rel=1e-6)
