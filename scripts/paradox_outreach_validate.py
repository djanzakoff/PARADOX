"""Validate PARADOX outreach draft files without sending email."""
from pathlib import Path
import csv

DATA = Path("outreach/restaurants.csv")
REQUIRED = {"restaurant", "email", "subject", "body", "approved"}

def main():
    if not DATA.exists():
        print("No outreach CSV yet. Add approved drafts before running.")
        return 0
    with DATA.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if not REQUIRED.issubset(reader.fieldnames or []):
            print("Missing required columns:", sorted(REQUIRED - set(reader.fieldnames or [])))
            return 1
        rows = list(reader)
    if len(rows) != 10:
        print(f"Expected 10 drafts, found {len(rows)}")
        return 1
    for i, row in enumerate(rows, 1):
        if not row["restaurant"].strip() or "@" not in row["email"] or not row["subject"].strip() or not row["body"].strip():
            print(f"Incomplete draft in row {i}")
            return 1
    print("Validated 10 drafts. No emails were sent.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
