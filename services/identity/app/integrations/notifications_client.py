"""
Notifications Client for ZAYVORA — SMS and Email.

Supports Twilio (SMS), SendGrid/SMTP (email), and gracefully falls back
to logging when API keys are absent (dev mode).
"""
from __future__ import annotations

import logging
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)


def _dev_mode() -> bool:
    return not os.environ.get("TWILIO_ACCOUNT_SID") and not os.environ.get("SENDGRID_API_KEY")


class NotificationsClient:
    """Unified SMS + Email notification client."""

    # ------------------------------------------------------------------
    # SMS
    # ------------------------------------------------------------------

    def send_sms(self, phone: str, message: str) -> bool:
        """Send an SMS via Twilio. Falls back to logging in dev mode."""
        if _dev_mode():
            logger.info("[DEV] SMS to %s: %s", phone, message)
            return True
        try:
            from twilio.rest import Client
            client = Client(os.environ["TWILIO_ACCOUNT_SID"], os.environ["TWILIO_AUTH_TOKEN"])
            msg = client.messages.create(body=message, from_=os.environ.get("TWILIO_FROM_NUMBER", ""), to=phone)
            logger.info("SMS sent: %s → %s", msg.sid, phone)
            return True
        except Exception as exc:
            logger.error("SMS send failed: %s", exc)
            return False

    def send_otp(self, phone_or_email: str, otp_code: str) -> bool:
        """Send a one-time password via SMS or email depending on the recipient format."""
        message = f"Your ZAYVORA verification code is: {otp_code}. Valid for 10 minutes. Do not share this code."
        if "@" in phone_or_email:
            return self.send_email(
                to=phone_or_email,
                subject="ZAYVORA Verification Code",
                html_body=f"<p>Your verification code is: <strong>{otp_code}</strong></p><p>Valid for 10 minutes.</p>",
                text_body=message,
            )
        return self.send_sms(phone_or_email, message)

    def send_appointment_reminder(self, patient_phone: str, appointment_details: dict) -> bool:
        """Send an appointment reminder SMS."""
        dt = appointment_details.get("datetime", "your scheduled time")
        doctor = appointment_details.get("doctor_name", "your doctor")
        clinic = appointment_details.get("clinic_name", "the clinic")
        message = (
            f"Reminder: You have an appointment with {doctor} at {clinic} on {dt}. "
            "Reply CANCEL to cancel or call us for changes."
        )
        return self.send_sms(patient_phone, message)

    # ------------------------------------------------------------------
    # Email
    # ------------------------------------------------------------------

    def send_email(self, to: str, subject: str, html_body: str, text_body: str = "") -> bool:
        """Send an email via SendGrid or SMTP fallback."""
        if _dev_mode():
            logger.info("[DEV] Email to %s | Subject: %s\n%s", to, subject, text_body or html_body)
            return True

        # Try SendGrid first
        sg_key = os.environ.get("SENDGRID_API_KEY")
        if sg_key:
            try:
                import sendgrid
                from sendgrid.helpers.mail import Mail
                sg = sendgrid.SendGridAPIClient(api_key=sg_key)
                mail = Mail(
                    from_email=os.environ.get("SMTP_USER", "noreply@zayvora.com"),
                    to_emails=to, subject=subject,
                    html_content=html_body, plain_text_content=text_body,
                )
                response = sg.send(mail)
                logger.info("SendGrid email sent to %s: status %s", to, response.status_code)
                return True
            except Exception as exc:
                logger.warning("SendGrid failed, trying SMTP: %s", exc)

        # SMTP fallback
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = os.environ.get("SMTP_USER", "noreply@zayvora.com")
            msg["To"] = to
            if text_body:
                msg.attach(MIMEText(text_body, "plain"))
            msg.attach(MIMEText(html_body, "html"))

            with smtplib.SMTP(
                os.environ.get("SMTP_HOST", "localhost"),
                int(os.environ.get("SMTP_PORT", "587")),
            ) as server:
                server.starttls()
                user = os.environ.get("SMTP_USER", "")
                pwd = os.environ.get("SMTP_PASSWORD", "")
                if user and pwd:
                    server.login(user, pwd)
                server.sendmail(msg["From"], to, msg.as_string())
            logger.info("SMTP email sent to %s", to)
            return True
        except Exception as exc:
            logger.error("Email send failed: %s", exc)
            return False
