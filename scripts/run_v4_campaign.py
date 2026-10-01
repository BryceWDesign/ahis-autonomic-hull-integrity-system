"""Regenerate v4 synthetic evidence using the declared reference request."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from ahis.survival.campaign import run_campaign
from ahis.survival.numeric import load_json
if __name__=="__main__":
    result=run_campaign(load_json(ROOT/"configs/survival_reference.json"),ROOT/"results/v4_survival_campaign")
    print("v4 cases=",len(result["cases"])," all_pass=",result["all_pass"])
    raise SystemExit(0 if result["all_pass"] else 1)
