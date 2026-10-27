"""Send ten explicitly approved PARADOX restaurant proposals via Mail.ru SMTP."""
import csv
import os
import smtplib
import ssl
import sys
from email.message import EmailMessage
from pathlib import Path

SENDER = "paradoxmenu@mail.ru"
DATA = Path("outreach/restaurants.csv")

def main():
    if os.environ.get("PARADOX_CONFIRM_SEND") != "SEND-10":
        print("Not authorized for sending.")
        return 2
    password = os.environ.get("PARADOX_MAILRU_APP_PASSWORD", "").strip()
    if not password:
        print("Mail.ru secret is missing.")
        return 2
    with DATA.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 10 or any(r["approved"] != "yes" for r in rows):
        print("Expected exactly ten approved messages.")
        return 2
    if len({r["email"].strip().lower() for r in rows}) != 10:
        print("Duplicate recipient.")
        return 2
    with smtplib.SMTP_SSL("smtp.mail.ru", 465, timeout=30, context=ssl.create_default_context()) as smtp:
        smtp.login(SENDER, password)
        for i, r in enumerate(rows, 1):
            msg = EmailMessage()
            msg["From"] = SENDER
            msg["To"] = r["email"]
            msg["Subject"] = r["subject"]
            msg.set_content(r["body"])
            refused = smtp.send_message(msg, from_addr=SENDER, to_addrs=[r["email"]])
            if refused:
                print(f"REJECTED {i}: {r['restaurant']}")
                return 3
            print(f"ACCEPTED {i}: {r['restaurant']}")
    print("SMTP accepted all ten messages.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
