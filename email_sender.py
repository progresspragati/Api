from dotenv import load_dotenv
import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

SENDER_EMAIL = os.getenv("EMAIL_SENDER")
SENDER_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")   # NOT normal password
RECEIVER_EMAILS = ["progresspragatigupta@gmail.com",
                   "ravi@connectingit.in",
                   "ritesh.k@consultit.co.in",
                   "vinod.gupta@consultit.co.in"]



def send_email(subject, body, attachment_path):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = ", ".join(RECEIVER_EMAILS) 
    msg["Subject"] = "Esimfx, Zetexa Balance, Airalo Orders"

    msg.attach(MIMEText(body, "plain"))

     # 🔹 Attach screenshot
    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())

        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={os.path.basename(attachment_path)}",
        )
        msg.attach(part)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(
            SENDER_EMAIL,
            RECEIVER_EMAILS,   # actual list goes here
            msg.as_string()
        )
