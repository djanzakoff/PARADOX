import csv,os,smtplib,ssl
from email.message import EmailMessage
from pathlib import Path
p=Path("outreach/massage.csv")
rows=list(csv.DictReader(p.open(encoding="utf-8",newline="")))
assert len(rows)==10 and all(r["approved"]=="yes" for r in rows)
assert len(set(r["email"].lower() for r in rows))==10
if os.getenv("PARADOX_CONFIRM_MASSAGE")!="SEND-MASSAGE-10": raise SystemExit("Not authorized")
password=os.getenv("PARADOX_MAILRU_APP_PASSWORD")
if not password: raise SystemExit("Missing Mail.ru password")
with smtplib.SMTP_SSL("smtp.mail.ru",465,timeout=30,context=ssl.create_default_context()) as smtp:
 smtp.login("paradoxmenu@mail.ru",password)
 for i,r in enumerate(rows,1):
  msg=EmailMessage();msg["From"]="paradoxmenu@mail.ru";msg["To"]=r["email"];msg["Subject"]=r["subject"];msg.set_content(r["body"])
  refused=smtp.send_message(msg,from_addr="paradoxmenu@mail.ru",to_addrs=[r["email"]])
  if refused: raise SystemExit(f"REJECTED {i}: {r['salon']}")
  print(f"ACCEPTED {i}: {r['salon']}")
print("SMTP accepted all ten massage messages.")
