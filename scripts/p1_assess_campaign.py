#!/usr/bin/env python3
"""Assess exactly three AHIS-P1 physical run records; never edits PHYSICAL_STATUS.json."""
from __future__ import annotations
from dataclasses import fields
from hashlib import sha256
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'src'
if str(SRC) not in sys.path: sys.path.insert(0,str(SRC))
from ahis.physical import P1RunEvidence, assess_p1_campaign

def main(argv:list[str])->int:
    if len(argv)!=5:
        print('usage: python scripts/p1_assess_campaign.py <run1.json> <run2.json> <run3.json> <out.json>',file=sys.stderr); return 2
    names={f.name for f in fields(P1RunEvidence)}
    runs=[]; inputs=[]
    for value in argv[1:4]:
        p=Path(value).resolve(); raw=json.loads(p.read_text(encoding='utf-8'))
        missing=names-set(raw)
        if missing: raise ValueError(f'{p} missing fields: {sorted(missing)}')
        runs.append(P1RunEvidence(**{n:raw[n] for n in names}))
        inputs.append({'path':p.name,'sha256':sha256(p.read_bytes()).hexdigest()})
    result=assess_p1_campaign(runs)
    payload={'schema_version':'1.0','source_kind':'PHYSICAL_CAMPAIGN_ASSESSMENT','inputs':inputs,'assessment':result,
             'claim_boundary':'P1_LOW_ENERGY_LEAK_SEAL_ONLY__NO_STRUCTURAL_STRENGTH_OR_HULL_SURVIVABILITY_CREDIT',
             'automatic_status_promotion':False}
    digest=sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    payload['receipt_sha256']=digest
    out=Path(argv[4]); out.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(out); return 0 if result['physical_demonstration'] else 1
if __name__=='__main__': raise SystemExit(main(sys.argv))
