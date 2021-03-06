import sendgrid
import os
from sendgrid.helpers.mail import *
from flask import render_template, current_app


def auth_email(from_email, subject, to_email, content):
    sg = sendgrid.SendGridAPIClient(apikey=current_app.config['SENDGRID_API_KEY'])
    from_email = Email("flaskframe-verify@davidcrandall.com")
    to_email = Email(to_email)
    content = Content("text/html", content)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    if response.status_code != 202:
        return response.status_code
    return 202


def reset_email(from_email, subject, to_email, content):
    sg = sendgrid.SendGridAPIClient(apikey=current_app.config['SENDGRID_API_KEY'])
    from_email = Email("flaskframe-reset@davidcrandall.com")
    to_email = Email(to_email)
    content = Content("text/html", content)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    if response.status_code != 202:
        return False
    return True
