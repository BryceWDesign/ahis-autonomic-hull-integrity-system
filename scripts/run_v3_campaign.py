#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ahis.campaign_v3 import run_campaign
from ahis.evidence import digest_json


def main() -> int:
    out = ROOT / "results" / "v3_extreme_campaign"
    out.mkdir(parents=True, exist_ok=True)
    campaign = run_campaign()
    campaign_path = out / "campaign.json"
    campaign_path.write_text(json.dumps(campaign, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    receipt = {
        "artifact": "campaign.json",
        "sha256_canonical_json": digest_json(campaign),
        "authority": campaign["authority"],
        "all_pass_conditions": all(campaign["pass_conditions"].values()),
    }
    receipt_path = out / "receipt.json"
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"campaign={campaign_path.relative_to(ROOT)}")
    print(f"receipt={receipt_path.relative_to(ROOT)}")
    print(f"all_pass_conditions={receipt['all_pass_conditions']}")
    return 0 if receipt["all_pass_conditions"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
