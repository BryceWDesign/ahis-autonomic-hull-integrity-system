from ahis.campaign import run_campaign


def test_extreme_campaign_all_pass():
    r = run_campaign()
    assert all(r["pass_conditions"].values())
    assert r["authority"].endswith("NO_PHYSICAL_SURVIVAL_OR_HEALING_CREDIT")
    assert r["positive_case"]["healing_decision"]["structural_restoration_credit"] == 0
