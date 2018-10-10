import sendgrid
import os
from sendgrid.helpers.mail import *
from app import app
from flask import render_template

def send_email(from_email, subject, to_email, content):
    sg = sendgrid.SendGridAPIClient(apikey=app.config['SENDGRID_API_KEY'])
    from_email = Email("cool@davidcrandall.com")
    to_email = Email(to_email)
    content = Content("text/html", content)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    if response.status_code != 202:
        return 'there was an error'
    return 'Sent'
