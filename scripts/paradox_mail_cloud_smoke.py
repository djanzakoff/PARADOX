"""Single-recipient Mail.ru SMTP smoke test for PARADOX.

Only sends to the same verified business mailbox. No bulk sending.
Credential must be supplied by GitHub Actions secret.
"""
import os
import smtplib
import ssl
import sys
from email.message import EmailMessage
from email.utils import formatdate, make_msgid

MAILBOX = "paradoxmenu@mail.ru"


def main():
    password = os.environ.get("PARADOX_MAILRU_APP_PASSWORD", "").strip()
    if not password:
        print(
            "NO_SECRET: Add PARADOX_MAILRU_APP_PASSWORD under "
            "Settings > Secrets and variables > Actions.",
            file=sys.stderr,
        )
        return 2

    message = EmailMessage()
    message["From"] = MAILBOX
    message["To"] = MAILBOX
    message["Subject"] = "PARADOX: тест облачной отправки Mail.ru"
    message["Date"] = formatdate(localtime=False)
    message["Message-ID"] = make_msgid(domain="paradoxmenu.ru")
    message.set_content(
        "Это безопасный тест облачной отправки PARADOX через GitHub Actions.\n"
        "Отправитель и получатель: paradoxmenu@mail.ru.\n"
        "Коммерческие предложения ресторанам не отправлялись.\n"
    )

    try:
        with smtplib.SMTP_SSL(
            "smtp.mail.ru",
            465,
            timeout=25,
            context=ssl.create_default_context(),
        ) as smtp:
            smtp.login(MAILBOX, password)
            refused = smtp.send_message(
                message, from_addr=MAILBOX, to_addrs=[MAILBOX]
            )
            if refused:
                print("SMTP_REFUSED: recipient was rejected.", file=sys.stderr)
                return 3
    except (OSError, smtplib.SMTPException):
        # Avoid logging SMTP authentication errors containing private details.
        print("SMTP_ERROR: Mail.ru did not accept the cloud message.", file=sys.stderr)
        return 4

    print("SMTP_ACCEPTED: self-test message accepted by Mail.ru.")
    print("Check the mailbox paradoxmenu@mail.ru to confirm delivery.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
