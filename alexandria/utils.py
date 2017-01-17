# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
import regex as r
from flask import flash, render_template, current_app

def flash_errors(form, category="warning"):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}"
                  .format(getattr(form, field).label.text, error), category)

def parse_search_params(searchterm):
    parsed_term = r.sub(u"\p{P}+", " ",searchterm).split()
    if len(parsed_term) == 1:
        return parsed_term[0]
    else:
        parsed_term = '&'.join(parsed_term)
    return parsed_term
