# encoding: utf-8

from functools import wraps
from flask import abort

from app.auth.models import Invite


def get_email(func):
    """
        Ensure that invite_str is correct.
        If correct than marks all invites that they are used and pass email to func,
        else raises 404 error page.
    """

    @wraps(func)
    def wrapper(invite_str):
        invite = Invite.query.filter_by(invite=invite_str).filter_by(used=False).first()
        if invite:
            tmp = func(invite_str, invite.email)
            email_invites = Invite.query.filter_by(email=invite.email).filter_by(used=False).all()
            for inv in email_invites:
                inv.update(used=True)

            return tmp
        else:
            abort(404)

    return wrapper
