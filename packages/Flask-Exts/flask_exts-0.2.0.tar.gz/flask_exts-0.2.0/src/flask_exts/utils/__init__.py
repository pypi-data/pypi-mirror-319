from flask import flash
from flask_babel import gettext
from .url import get_redirect_target


def flash_errors(form, message):
    for field_name, errors in form.errors.items():
        errors = form[field_name].label.text + ": " + ", ".join(errors)
        flash(gettext(message, error=str(errors)), "error")
