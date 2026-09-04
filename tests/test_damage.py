from math import hypot
import pytest
from ahis.damage import SensorReading, localize_event


def make_readings(x=0.32, y=0.68, speed=2500.0, t0=0.01, failed=()):
    coords = {"a":(0,0),"b":(1,0),"c":(1,1),"d":(0,1),"e":(0.5,0),"f":(0.5,1)}
    return [SensorReading(k,sx,sy,t0+hypot(x-sx,y-sy)/speed,1.0,k not in failed) for k,(sx,sy) in coords.items()]


def test_localization_accuracy():
    est = localize_event(make_readings(), wave_speed_m_s=2500, panel_bounds_m=(0,1,0,1), amplitude_threshold=.2, grid_points_per_axis=81, max_residual_s=8e-5)
    assert est.detected
    assert hypot(est.x_m-.32, est.y_m-.68) < .03
    assert est.confidence > .5


def test_insufficient_quorum_fails():
    est = localize_event(make_readings(failed=("a","b","c")), wave_speed_m_s=2500, panel_bounds_m=(0,1,0,1), amplitude_threshold=.2, min_sensors=4)
    assert not est.detected
    assert est.confidence == 0


def test_duplicate_sensor_rejected():
    r = make_readings()[:4]
    r.append(r[0])
    with pytest.raises(ValueError):
        localize_event(r, wave_speed_m_s=2500, panel_bounds_m=(0,1,0,1), amplitude_threshold=.2)


def test_bad_bounds_rejected():
    with pytest.raises(ValueError):
        localize_event(make_readings(), wave_speed_m_s=2500, panel_bounds_m=(1,0,0,1), amplitude_threshold=.2)


def test_negative_amplitude_rejected():
    r = make_readings(); r[0] = SensorReading("a",0,0,.1,-1,True)
    with pytest.raises(ValueError):
        localize_event(r, wave_speed_m_s=2500, panel_bounds_m=(0,1,0,1), amplitude_threshold=.2)
