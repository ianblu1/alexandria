# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from flask import flash, render_template, current_app
# from wtforms import BooleanField
# from wtforms.widgets.core import html_params
# from wtforms.widgets import HTMLString

def flash_errors(form, category="warning"):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}"
                  .format(getattr(form, field).label.text, error), category)

# class InlineButtonWidget(object):
#     """
#     Render a basic ``<button>`` field.
#     """
#     input_type = 'submit'
#     html_params = staticmethod(html_params)

#     def __call__(self, field, **kwargs):
#         kwargs.setdefault('id', field.id)
#         kwargs.setdefault('type', self.input_type)
#         #kwargs.setdefault('value', field.label.text)
#         kwargs.setdefault('value', "submitted")
#         #kwargs.setdefault('default', "submit")
#         return HTMLString('<button %s>Submit</button>' % self.html_params(name=field.name, **kwargs))


# class ButtonSubmitField(BooleanField):
#     """
#     Represents an ``<button type="submit">``.  This allows checking if a given
#     submit button has been pressed.
#     """
#     widget = InlineButtonWidget()
