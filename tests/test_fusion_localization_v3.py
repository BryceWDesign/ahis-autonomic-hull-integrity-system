from math import hypot
import pytest

from ahis.fusion import EvidenceChannel, fuse_evidence
from ahis.localization_v3 import AnisotropicPropagation, ArrivalObservation, localize_anisotropic


def make_arrivals(x=0.4, y=0.6):
    model = AnisotropicPropagation(2400, 0.1, 15)
    coords = [("1",0,0),("2",1,0),("3",1,1),("4",0,1),("5",0.5,0),("6",0.5,1)]
    rows=[]
    for sid,sx,sy in coords:
        dx,dy=x-sx,y-sy
        rows.append(ArrivalObservation(sid,sx,sy,0.01+hypot(dx,dy)/model.speed(dx,dy),1))
    return model, rows


def test_multimodal_fusion_accepts_consistent_damage():
    result = fuse_evidence([EvidenceChannel("a",.9,1), EvidenceChannel("b",.85,1), EvidenceChannel("c",.8,.8)])
    assert result.accepted
    assert result.disagreement < .1


def test_multimodal_fusion_rejects_low_quality_quorum():
    result = fuse_evidence([EvidenceChannel("a",.99,.2), EvidenceChannel("b",.99,.2)])
    assert not result.accepted
    assert "insufficient" in result.reason


def test_disagreement_penalizes_fused_score():
    consistent = fuse_evidence([EvidenceChannel("a",.8,1), EvidenceChannel("b",.8,1)], min_effective_weight=1)
    conflict = fuse_evidence([EvidenceChannel("a",1,1), EvidenceChannel("b",.6,1)], min_effective_weight=1)
    assert conflict.fused_damage_score < consistent.fused_damage_score


def test_anisotropic_localization_recovers_known_event():
    model, rows = make_arrivals()
    result = localize_anisotropic(rows, model=model, bounds_m=(0,1,0,1), grid_points_per_axis=81)
    assert result.accepted
    assert result.x_m == pytest.approx(.4, abs=.013)
    assert result.y_m == pytest.approx(.6, abs=.013)
    assert result.confidence_radius_m is not None


def test_localization_rejects_sensor_quality_loss():
    model, rows = make_arrivals()
    rows = [ArrivalObservation(r.sensor_id,r.x_m,r.y_m,r.arrival_s,.2) for r in rows]
    result = localize_anisotropic(rows, model=model, bounds_m=(0,1,0,1))
    assert not result.accepted
    assert "insufficient" in result.reason


def test_anisotropy_validation():
    with pytest.raises(ValueError):
        AnisotropicPropagation(2400, .9, 0)
