import smtplib
from email.mime.text import MIMEText
from config import settings





def send_email(to_email: str, subject: str, body: str):
    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["From"] = settings.SMTP_EMAIL
    msg["To"] = to_email

    with smtplib.SMTP(settings.SMTP_SERVER, 587) as server:  # Replace with correct SMTP server
  
        server.starttls()
        server.login(settings.SMTP_EMAIL, settings.SMTP_PASSWORD)  # Use environment variables for security

        # server.starttls()
        # server.login(settings.SMTP_EMAIL, settings.SMTP_PASSWORD)
        server.sendmail(settings.SMTP_EMAIL, to_email, msg.as_string())
