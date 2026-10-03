#!/usr/bin/env python3
"""Validate decision-object records against the JSON Schema plus the cross-field rules it can't express.

Usage:  uv run --no-project --with jsonschema python validate.py [files...]
        (default: every examples/**/*.json)
"""
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve().parent
SCHEMA_PATH = HERE / "schema" / "v0.3" / "decision-object.schema.json"
schema = json.loads(SCHEMA_PATH.read_text())
Draft202012Validator.check_schema(schema)
validator = Draft202012Validator(schema)


def semantic_errors(doc: dict) -> list[str]:
    """Cross-field rules from README § "Rules the schema cannot express"."""
    errs = []
    req = doc.get("request", {})
    resp = doc.get("response")
    ack = doc.get("ack")
    keys = [o["key"] for o in req.get("options", [])]

    if len(keys) != len(set(keys)):
        errs.append("options[].key must be unique")
    if "rec" in req and req["rec"] not in keys:
        errs.append(f"rec '{req['rec']}' is not one of options[].key {keys}")
    if req.get("risk") and req.get("on_expiry", "nothing") != "nothing":
        errs.append("on_expiry must be 'nothing' when risk is non-empty")

    if resp:
        choice = resp.get("choice")
        if choice is not None:
            allowed = keys + (["done"] if req.get("kind") in ("task", "command") else []) \
                + (["read"] if req.get("kind") == "brief" else [])
            if choice not in allowed:
                errs.append(f"response.choice '{choice}' not in {allowed}")
        if resp.get("decided_by") == "rule" and req.get("risk"):
            errs.append("a request with risk tags must never be decided by a rule")
        if resp.get("decided_by") == "expiry":
            if req.get("on_expiry") != "proceed_with_rec":
                errs.append("decided_by 'expiry' requires request.on_expiry = proceed_with_rec")
            if req.get("risk"):
                errs.append("a request with risk tags must never be decided by expiry")
            if choice != req.get("rec"):
                errs.append("decided_by 'expiry' must choose request.rec")
        if resp.get("status") == "done" and req.get("kind") not in ("task", "command", "brief"):
            errs.append("status 'done' is for task/command/brief; decisions use 'decided'")
        if req.get("kind") == "brief" and resp.get("status") == "decided":
            errs.append("a brief is never 'decided'; reading it is status 'done' with choice 'read'")
    if ack and not resp:
        errs.append("ack without a response")
    if ack and resp and resp.get("status") in ("open", "withdrawn"):
        errs.append(f"ack on a request whose status is '{resp['status']}'")
    return errs


def main(paths: list[str]) -> int:
    files = [Path(p).resolve() for p in paths] or sorted((HERE / "examples").rglob("*.json"))
    bad = 0
    for f in files:
        name = f.relative_to(HERE) if HERE in f.parents else f
        try:
            doc = json.loads(f.read_text())
        except (OSError, json.JSONDecodeError) as exc:
            print(f"FAIL {name}\n     - invalid JSON: {exc}")
            bad += 1
            continue
        errs = [f"{'/'.join(map(str, e.absolute_path)) or '<root>'}: {e.message}"
                for e in validator.iter_errors(doc)]
        if not errs:
            errs = semantic_errors(doc)
        print(f"{'OK  ' if not errs else 'FAIL'} {name}")
        for e in errs:
            print(f"     - {e}")
        bad += bool(errs)
    print(f"\n{len(files) - bad}/{len(files)} valid")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
