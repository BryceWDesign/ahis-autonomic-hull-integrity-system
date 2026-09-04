from pathlib import Path
import importlib.util
import sys
import pytest

ROOT = Path(__file__).resolve().parents[1]

def load(name):
    p=ROOT/"src"/"analysis"/f"{name}.py"
    spec=importlib.util.spec_from_file_location(name,p); m=importlib.util.module_from_spec(spec); sys.modules[name]=m; spec.loader.exec_module(m); return m


def test_normalization_math():
    m=load("normalization_utils")
    assert m.areal_density_kg_m2(mass_kg=2,area_m2=.5)==4
    assert m.added_mass_fraction_percent(baseline_mass_kg=1,test_mass_kg=1.2)==pytest.approx(20)


def test_normalization_rejects_bad_values():
    m=load("normalization_utils")
    with pytest.raises(ValueError): m.areal_density_kg_m2(mass_kg=1,area_m2=0)
