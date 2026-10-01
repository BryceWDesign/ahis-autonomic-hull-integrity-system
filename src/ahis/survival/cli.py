"""Portable CLI for evidence decisions, demonstrations and deterministic replay."""

import argparse
import json
from pathlib import Path
from .numeric import load_json, write_json
from .replay_audit import record, audit


def main(argv=None):
    parser = argparse.ArgumentParser(prog="ahis")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("decide", help="evaluate an archived synthetic request")
    p.add_argument("request", type=Path)
    p.add_argument("--out", type=Path, required=True)
    p = sub.add_parser("audit", help="reconstruct a decision from raw archived evidence")
    p.add_argument("bundle", type=Path)
    p.add_argument("--trusted-digest")
    p = sub.add_parser("campaign", help="run reference and negative-control cases")
    p.add_argument("--config", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "decide":
            result = record(load_json(args.request))
            write_json(args.out, result)
            print(
                json.dumps(
                    {
                        "state": result["result"]["state"],
                        "digest": result["sha256"],
                        "hardware_authority": False,
                    }
                )
            )
            return 0 if result["result"]["state"] == "RECOVERED_LIMITED" else 2
        if args.command == "audit":
            result = audit(load_json(args.bundle), trusted_digest=args.trusted_digest)
            print(json.dumps(result))
            return 0 if result["passed"] else 1
        from .campaign import run_campaign

        result = run_campaign(load_json(args.config), args.out)
        print(json.dumps({"all_pass": result["all_pass"], "cases": len(result["cases"])}))
        return 0 if result["all_pass"] else 1
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(json.dumps({"error": str(exc), "hardware_authority": False}))
        return 1
