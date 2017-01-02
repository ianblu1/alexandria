# -*- coding: utf-8 -*-
"""Functional tests using WebTest.

See: http://webtest.readthedocs.org/
"""
import pytest
from flask import url_for


from alexandria.models.users import User
from .factories import UserFactory


class TestLoggingIn:

    def test_log_in_and_redirect_returns_302(self, user, testapp):
        # Goes to homepage
        res = testapp.get("/")
        # Fills out login form in navbar
        form = res.forms['loginForm']
        form['username'] = user.user_name
        form['password'] = 'myprecious'
        # Submits
        res = form.submit().follow()
        assert res.status_code == 302

    def test_sees_alert_on_log_out(self, user, testapp):
        res = testapp.get("/")
        # Fills out login form in navbar
        form = res.forms['loginForm']
        form['username'] = user.user_name
        form['password'] = 'myprecious'
        # Submits
        res = form.submit().follow()
        res = testapp.get(url_for('public.logout')).follow()
        # sees alert
        assert 'You are logged out.' in res

    def test_sees_error_message_if_password_is_incorrect(self, user, testapp):
        # Goes to homepage
        res = testapp.get("/")
        # Fills out login form, password incorrect
        form = res.forms['loginForm']
        form['username'] = user.user_name
        form['password'] = 'wrong'
        # Submits
        res = form.submit()
        # sees error
        assert "Invalid password" in res

    def test_sees_error_message_if_username_doesnt_exist(self, user, testapp):
        # Goes to homepage
        res = testapp.get("/")
        # Fills out login form, password incorrect
        form = res.forms['loginForm']
        form['username'] = 'unknown'
        form['password'] = 'myprecious'
        # Submits
        res = form.submit()
        # sees error
        assert "Unknown user" in res

        