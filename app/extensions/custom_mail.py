# encoding: utf-8

from flask_mail import Mail


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
