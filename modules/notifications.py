"""Email notification helpers for contact messages."""
from __future__ import annotations
import smtplib
from email.message import EmailMessage
from typing import Optional


def send_contact_notification(message: dict, config: dict) -> None:
    """Send an email notification for a new contact message.

    Expects `config` to contain SMTP configuration keys:
      - SMTP_HOST
      - SMTP_PORT
      - SMTP_USER (optional)
      - SMTP_PASSWORD (optional)
      - MAIL_FROM
      - MAIL_TO
      - SMTP_USE_SSL (optional, bool)

    The function is best-effort and will raise on failure so callers can handle it.
    """
    host = config.get("SMTP_HOST")
    port = int(config.get("SMTP_PORT", 0) or 0)
    user = config.get("SMTP_USER")
    password = config.get("SMTP_PASSWORD")
    mail_from = config.get("MAIL_FROM")
    mail_to = config.get("MAIL_TO")
    use_ssl = bool(config.get("SMTP_USE_SSL"))

    if not host or not port or not mail_from or not mail_to:
        raise ValueError("Incomplete SMTP configuration")

    body = []
    body.append(f"Name: {message.get('name')}")
    body.append(f"Email: {message.get('email')}")
    body.append(f"Subject: {message.get('subject') or '(no subject)'}")
    body.append("")
    body.append(message.get("message", ""))
    body_text = "\n".join(body)

    subject = f"New contact: {message.get('subject') or 'Message from website'}"

    email = EmailMessage()
    email["From"] = mail_from
    email["To"] = mail_to
    email["Subject"] = subject
    email.set_content(body_text)

    if use_ssl:
        smtp = smtplib.SMTP_SSL(host, port, timeout=10)
    else:
        smtp = smtplib.SMTP(host, port, timeout=10)

    try:
        if not use_ssl:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
        if user and password:
            smtp.login(user, password)
        smtp.send_message(email)
    finally:
        smtp.quit()


def send_confirmation_email(message: dict, config: dict) -> None:
    """Send a confirmation email back to the visitor who submitted the form.

    Uses `MAIL_FROM` as sender and `message['email']` as recipient.
    """
    print(message)

    print(config)
    host = config.get("SMTP_HOST")
    port = int(config.get("SMTP_PORT", 0) or 0)
    user = config.get("SMTP_USER")
    password = config.get("SMTP_PASSWORD")
    mail_from = config.get("MAIL_FROM")
    recipient = message.get("email")
    use_ssl = bool(config.get("SMTP_USE_SSL"))

    if not host or not port or not mail_from or not recipient:
        raise ValueError("Incomplete SMTP configuration for confirmation email")

    subject = "Thanks for contacting me — I received your message"
    body = (
        f"Hi {message.get('name')},\n\n"
        "Thanks for reaching out. I received your message and will respond within 24 hours.\n\n"
        "Your message:\n"
        "----------------\n"
        f"{message.get('message','')}\n\n"
        "—\nRegards"
    )

    email = EmailMessage()
    email["From"] = mail_from
    email["To"] = recipient
    email["Subject"] = subject
    email.set_content(body)

    if use_ssl:
        smtp = smtplib.SMTP_SSL(host, port, timeout=10)
    else:
        smtp = smtplib.SMTP(host, port, timeout=10)

    try:
        if not use_ssl:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
        if user and password:
            smtp.login(user, password)
        smtp.send_message(email)
    finally:
        smtp.quit()
