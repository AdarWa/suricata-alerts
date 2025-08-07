import smtplib, ssl
from email.message import EmailMessage
import logging

class Mailer:
    
    def __init__(self, mailer_type="SMTP", port=587, smtp_server="smtp.zeptomail.com", username="", password=""):
        self.mailer_type = mailer_type
        if mailer_type != "SMTP":
            raise TypeError("No mailer other than SMTP!")
        if not username or not password:
            raise TypeError("Username and password must be set!")
        if port != 465 and port != 587:
            raise TypeError("Port must be 465 or 587!")
        self.port = port
        self.smtp_server = smtp_server
        self.username=username
        self.password = password
    
    def send_message(self, from_email, to_email, subject, message):
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email
        msg.set_content(message)
        try:
            if self.port == 465:
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
                    server.login(self.username, self.password)
                    server.send_message(msg)
            elif self.port == 587:
                with smtplib.SMTP(self.smtp_server, self.port) as server:
                    server.starttls()
                    server.login(self.username, self.password)
                    server.send_message(msg)
            logging.info("Successfuly sent email to "+ to_email + " from " + from_email)
        except Exception as e:
            logging.exception("Exception occured while sending email: " + str(e))