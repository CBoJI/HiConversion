# encoding: utf-8

import smtplib
from flask import current_app
from flask_mail import Mail, Message


class CustomMail(Mail):

    def send(self, message):
        """Overwrite method of Mail.send.
        Sends a single message instance.
        Actually it prints it out to the console.
        :param message: a Message instance.
        """
        print '*' * 80
        print message
        print '*' * 80

    def send_invite(self, email):

        from app.auth.models import Invite
        inv = Invite.create_invite(email)
        msg = Message("Hello",
                      body='testing\n invite: %s' % inv.invite,
                      sender="no-replay@example.com",
                      recipients=[email, ])

        return self.try_to_send(msg)

    def send_login_info(self, email, password):
        msg = Message("Hello",
                      body='testing\n login: %s\n password: %s' % (email, password),
                      sender="no-replay@example.com",
                      recipients=[email, ])

        return self.try_to_send(msg)

    def try_to_send(self, msg):
        try:
            self.send(msg)
        except smtplib.SMTPAuthenticationError, e:
            current_app.logger.error(e.message)
            return False
        except smtplib.SMTPServerDisconnected, e:
            current_app.logger.error(e.message)
            return False
        except smtplib.SMTPException, e:
            current_app.logger.error(e.message)
            return False

        return True
