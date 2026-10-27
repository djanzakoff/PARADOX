"""Validate arbitrary-size PARADOX email campaigns before an approved send.

CSV columns: restaurant,email,subject,body,approved
This command never sends email.
"""
import argparse
import csv
from pathlib import Path

REQUIRED = {"restaurant", "email", "subject", "body", "approved"}

def validate(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        missing = REQUIRED - set(reader.fieldnames or [])
        if missing:
            raise ValueError("Missing columns: " + ", ".join(sorted(missing)))
        rows = list(reader)
    if not rows:
        raise ValueError("Empty campaign")
    seen = set()
    for i, row in enumerate(rows, 2):
        if any(not row[k].strip() for k in REQUIRED):
            raise ValueError(f"Empty field at CSV row {i}")
        if row["approved"].lower().strip() not in {"yes", "no"}:
            raise ValueError(f"Invalid approval at CSV row {i}")
        address = row["email"].strip().lower()
        if address.count("@") != 1 or " " in address:
            raise ValueError(f"Invalid email at CSV row {i}")
        if address in seen:
            raise ValueError(f"Duplicate email at CSV row {i}")
        seen.add(address)
    approved = sum(r["approved"].strip().lower() == "yes" for r in rows)
    print(f"VALID: {len(rows)} unique recipients, {approved} approved, {len(rows)-approved} pending.")
    return rows

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", nargs="?", default="outreach/restaurants.csv")
    args = parser.parse_args()
    try:
        validate(args.csv)
    except (OSError, ValueError) as exc:
        print(f"INVALID: {exc}")
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
