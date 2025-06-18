import smtplib
from config import EMAIL_USER, EMAIL_PASS, ALERT_RECIPIENT

def send_alert_email(site_url):
    subject = f"ALERT: {site_url} is down!"
    body = f"The website {site_url} appears to be offline."
    message = f"Subject: {subject}\n\n{body}"

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, ALERT_RECIPIENT, message)