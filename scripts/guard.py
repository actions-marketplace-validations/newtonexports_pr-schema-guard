#!/usr/bin/env python3
import argparse
import json
import os
import sys
from jsonschema import Draft7Validator

def parse_args():
    parser = argparse.ArgumentParser(description="PR Schema Guard")
    parser.add_argument("--schema", required=True, help="Path to JSON Schema")
    parser.add_argument("--target", required=True, help="Target data directory")
    return parser.parse_args()

def run():
    args = parse_args()
    if not os.path.exists(args.schema):
        print(f"::error::Schema file not found at: {args.schema}")
        sys.exit(1)

    with open(args.schema, "r", encoding="utf-8") as sf:
        schema = json.load(sf)
    validator = Draft7Validator(schema)

    if not os.path.exists(args.target):
        print(f"::error::Target directory not found: {args.target}")
        sys.exit(1)

    errors = []
    files_checked = 0

    for root, _, files in os.walk(args.target):
        for f in files:
            if f.endswith(".json"):
                files_checked += 1
                filepath = os.path.join(root, f)
                try:
                    with open(filepath, "r", encoding="utf-8") as jf:
                        data = json.load(jf)
                    for err in validator.iter_errors(data):
                        errors.append(f"{f} -> path '{list(err.path)}': {err.message}")
                except Exception as e:
                    errors.append(f"{f} -> Parse error: {str(e)}")

    if errors:
        print(f"::error::Schema validation failed on {len(errors)} point(s):")
        for err in errors:
            print(f"- {err}")
        sys.exit(1)

    print(f"::notice::Schema guard passed successfully. Checked {files_checked} file(s).")

if __name__ == "__main__":
    run()
