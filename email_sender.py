from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

SENDER_EMAIL = os.getenv("EMAIL_SENDER")
SENDER_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")   # NOT normal password
RECEIVER_EMAILS = ["progresspragatigupta@gmail.com",
                   "ravi@connectingit.in",
                   "vinod.gupta@consultit.co.in"]


def send_email(subject, body):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = ", ".join(RECEIVER_EMAILS) 
    msg["Subject"] = "Esimfx, Zetexa Balance"

    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(
            SENDER_EMAIL,
            RECEIVER_EMAILS,   # actual list goes here
            msg.as_string()
        )
