import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings

logger = logging.getLogger(__name__)


# =========================
# CORE EMAIL SENDER
# =========================
def send_email(
    *,
    to_email: str,
    subject: str,
    text_body: str,
    html_body: str | None = None,
) -> bool:
    """
    Sends an email using SMTP SSL.

    - Always sends plain text.
    - Sends HTML version when provided.
    """

    try:
        message = MIMEMultipart("alternative")

        message["From"] = settings.EMAIL_FROM
        message["To"] = to_email
        message["Subject"] = subject

        message.attach(MIMEText(text_body, "plain"))

        if html_body:
            message.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP_SSL(
            settings.SMTP_HOST,
            settings.SMTP_PORT,
            timeout=15,
        ) as server:

            server.login(
                settings.SMTP_USER,
                settings.SMTP_PASSWORD,
            )

            server.send_message(message)

        logger.info("Email sent successfully to %s", to_email)

        return True

    except Exception:
        logger.exception("Failed to send email.")
        return False


# =========================
# PASSWORD RESET EMAIL
# =========================
def send_reset_code_email(
    to_email: str,
    code: str,
) -> bool:

    subject = "Reset your Lenar password"

    text_body = f"""
Hello,

We received a request to reset your Lenar account password.

Verification Code

{code}

This verification code expires in 10 minutes.

If you didn't request this password reset, simply ignore this email.

— Lenar Security Team
"""

    html_body = f"""
<html>
<body style="font-family:Arial,sans-serif;background:#f5f5f5;padding:30px;">
<div style="max-width:520px;margin:auto;background:white;padding:30px;border-radius:12px;">

<h2 style="margin-top:0;">Reset your password</h2>

<p>We received a request to reset your Lenar account password.</p>

<p>Your verification code is:</p>

<div style="
font-size:32px;
font-weight:bold;
letter-spacing:8px;
text-align:center;
padding:20px;
background:#f3f4f6;
border-radius:8px;
margin:24px 0;
">
{code}
</div>

<p>This code expires in <strong>10 minutes</strong>.</p>

<p>If you didn't request this reset, you can safely ignore this email.</p>

<hr>

<p style="color:#666;font-size:13px;">
Lenar Security Team
</p>

</div>
</body>
</html>
"""

    return send_email(
        to_email=to_email,
        subject=subject,
        text_body=text_body,
        html_body=html_body,
    )


# =========================
# REGISTRATION VERIFICATION EMAIL
# =========================
def send_registration_code_email(
    to_email: str,
    code: str,
) -> bool:

    subject = "Verify your Lenar account"

    text_body = f"""
Welcome to Lenar!

Use the verification code below to complete your registration.

Verification Code

{code}

This code expires in 10 minutes.

If you didn't start this registration, you can safely ignore this email.

Welcome,
Lenar Team
"""

    html_body = f"""
<html>
<body style="font-family:Arial,sans-serif;background:#f5f5f5;padding:30px;">
<div style="max-width:520px;margin:auto;background:white;padding:30px;border-radius:12px;">

<h2 style="margin-top:0;">Welcome to Lenar</h2>

<p>Thanks for creating your account.</p>

<p>Use the verification code below to finish your registration.</p>

<div style="
font-size:32px;
font-weight:bold;
letter-spacing:8px;
text-align:center;
padding:20px;
background:#eef6ff;
border-radius:8px;
margin:24px 0;
color:#2563eb;
">
{code}
</div>

<p>This code expires in <strong>10 minutes</strong>.</p>

<p>If you didn't start this registration, simply ignore this email.</p>

<hr>

<p style="color:#666;font-size:13px;">
Welcome to Lenar.
</p>

</div>
</body>
</html>
"""

    return send_email(
        to_email=to_email,
        subject=subject,
        text_body=text_body,
        html_body=html_body,
    )