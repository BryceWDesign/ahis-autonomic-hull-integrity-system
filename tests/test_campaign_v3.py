from ahis.campaign_v3 import AUTHORITY, run_campaign


def test_v3_campaign_all_conditions_pass():
    result=run_campaign()
    assert all(result["pass_conditions"].values())


def test_v3_campaign_has_strict_claim_boundary():
    result=run_campaign()
    assert result["authority"]==AUTHORITY
    assert "NO_PHYSICAL_HEALING" in result["authority"]


def test_v3_campaign_negative_controls_present():
    result=run_campaign()
    assert not result["negative_controls"]["estop"]["allowed"]
    assert not result["negative_controls"]["overpressure"]["allowed"]
    assert not result["negative_controls"]["resource_depletion"]["allowed"]
