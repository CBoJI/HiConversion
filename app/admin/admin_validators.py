# -*- coding: utf-8 -*-

from wtforms import validators

MAX_LENGTHS = {
    'login': 30,
    'password': 60,
    'invite': 36,
    'email': 30
}


def length_check(form, field):
    """ Fix flask-admin error in processing max length of the field. """
    max_length = MAX_LENGTHS.get(field.name)
    if max_length and len(field.data) > max_length:
        raise validators.StopValidation(u'The field cannot be more than %s characters.' % max_length)
