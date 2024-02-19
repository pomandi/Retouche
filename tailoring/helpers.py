from .models import Customer
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests

def send_email(object_id):
    customer = Customer.objects.get(pk=object_id)
    email_content = customer.email_content
    tracking_link = f"https://retouche-ce58e7481386.herokuapp.com/en/tailoring/order-status/{customer.tracking_id}"
    email_content = f"{email_content}POMANDI MEN SUIT,  Track your order here: {tracking_link}"
    email = customer.email

    if email_content:
        text_message = MIMEText(email_content, 'plain')
        username = 'info@pomandi.com'
        password = 'YU5Z8Ta@KnMHDmC'

        msg = MIMEMultipart('mixed')
        sender = 'info@pomandi.com'
        recipient = email

        msg['Subject'] = 'Your Tailoring Service is Ready'
        msg['From'] = sender
        msg['To'] = recipient

        msg.attach(text_message)

        mailServer = smtplib.SMTP('mail.smtp2go.com', 2525)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(username, password)
        mailServer.sendmail(sender, recipient, msg.as_string())
        mailServer.close()

def send_sms(object_id):
    customer = Customer.objects.get(pk=object_id)
    tracking_link = f"https://retouche-ce58e7481386.herokuapp.com/en/tailoring/order-status/{customer.tracking_id}"
    sms_content = f"{customer.sms_content}POMANDI MEN SUIT,  Track your order here: {tracking_link}"
    phone_number = customer.phone

    api_key = "api-8784277C593411EE90A0F23C91BBF4A0"

    url = "https://api.smtp2go.com/v3/sms/send"

    data = {
        "api_key": api_key,
        "destination": [phone_number],
        "content": sms_content
    }

    response = requests.post(url, json=data)
