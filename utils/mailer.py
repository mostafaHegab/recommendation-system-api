from flask_mail import Mail, Message

class Mailer():
    mail = Mail()

    def __init__(self, app):
        Mailer.mail.init_app(app)
        print(Mailer.mail)

    @staticmethod
    def send_email(subject, body, sender, reciever):
        msg = Message(subject=subject, body=body, sender=sender, recipients=[reciever])
        return Mailer.mail.send(msg)