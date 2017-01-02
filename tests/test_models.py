# -*- coding: utf-8 -*-
"""Model unit tests."""
import datetime as dt

import pytest

from alexandria.extensions import db
from alexandria.models.users import User
from .factories import UserFactory

@pytest.mark.usefixtures('db')
class TestUser:

    def test_factory(self, db):
        user = UserFactory(password="myprecious")
        db.session.commit()
        assert bool(user.user_name)
        assert bool(user.emails)
        assert bool(user.created_at)
        assert user.is_admin is False
        assert user.active is True
        assert user.check_password('myprecious')

    def test_get_user(self):
        user = User('foo@bar.com', 'foo', 'fn', 'ln', 'foobarbaz')
        #user.save()
        db.session.add(user)
        db.session.commit()

        retrieved = User.query.get(user.user_name)
        assert retrieved == user

    def test_check_password(self):
        user = User('foo@bar.com', 'foo', 'fn', 'ln', 'foobarbaz')
        assert user.check_password('foobarbaz') is True
        assert user.check_password("barfoobaz") is False

    def test_change_password(self):
        user = User('foo@bar.com', 'foo', 'fn', 'ln', 'password')
        user.set_password('different_password')
        assert user.check_password('different_password') is True
        assert user.check_password("password") is False

    def test_add_email(self):
        user = User('foo@bar.com', 'foo', 'fn', 'ln', 'password')
        user.add_email('baz@bar.com')
        assert [user_email.email for user_email in user.emails] == ['foo@bar.com', 'baz@bar.com']

    def test_dupe_email(self):
        user = User('foo@bar.com', 'foo', 'fn', 'ln', 'foobarbaz')
        #user.save()
        db.session.add(user)
        db.session.commit()

        user2 = User('foo@bar.com', 'foo1', 'fn1', 'ln1', 'foobarbaz')
        db.session.add(user2)
        with pytest.raises(Exception) as e_info:
            db.session.commit()


    def test_dupe_username(self):
        user = User('foo@bar.com', 'foo', 'fn', 'ln', 'foobarbaz')
        #user.save()
        db.session.add(user)
        db.session.commit()

        user2 = User('foo1@bar.com', 'foo', 'fn1', 'ln1', 'foobarbaz')
        db.session.add(user2)
        with pytest.raises(Exception) as e_info:
            db.session.commit()


