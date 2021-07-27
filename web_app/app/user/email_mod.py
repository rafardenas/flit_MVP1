import sendgrid
import os
from sendgrid.helpers.mail import *
import smtplib, ssl
from email.message import EmailMessage
from typing import Text
from flask import render_template, current_app
from web_app.config2 import Config






def send_email(subject, recipients, text_body, html_body):
    """Helper to send email to password recovery
    """
    sg = sendgrid.SendGridAPIClient(api_key=Config.API_KEY_SENDGRID)
    from_email = Email("seguridad@cargamx.com")
    to_email = To(recipients)
    content = Content("text/plain", text_body)
    html_content=HtmlContent(html_body)
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)


def send_password_reset_email(user):
    """Use helper to actuall send the password recobvery email
    """
    token = user.get_reset_password_token()
    send_email('[CargaMX] Recupera tu contraseña',
               recipients=[user.email],
               text_body=render_template('user/reset_password_mail.txt',
                                         user=user, token=token),
               html_body=render_template('user/reset_password_mail.html',
                                         user=user, token=token))

