# -*- coding: utf-8 -*-
import pytest


from alexandria.forms import LoginForm, ChangePasswordForm, EmailForm
#from docufind.forms.user import RegisterForm
from .factories import UserFactory


# class TestRegisterForm:

#     def test_validate_user_already_registered(self, user):
#         # Enters username that is already registered
#         form = RegisterForm(username=user.username, email='foo@bar.com',
#             password='example', confirm='example')

#         assert form.validate() is False
#         assert 'Username already registered' in form.username.errors

#     def test_validate_email_already_registered(self, user):
#         # enters email that is already registered
#         form = RegisterForm(username='unique', email=user.email,
#             password='example', confirm='example')

#         assert form.validate() is False
#         assert 'Email already registered' in form.email.errors

#     def test_validate_success(self, db):
#         form = RegisterForm(username='newusername', email='new@test.test',
#             password='example', confirm='example')
#         assert form.validate() is True

#@pytest.mark.usefixtures('user')
class TestLoginForm:

    def test_validate_success(self, user, db):
        user.set_password('example')
        db.session.add(user)
        db.session.commit()
        #user.save()
        form = LoginForm(username=user.user_name, password='example')
        print(form.user)
        assert form.validate() is True
        assert form.user == user

    def test_validate_unknown_username(self, db):
        form = LoginForm(username='unknown', password='example')
        assert form.validate() is False
        assert 'Unknown username' in form.username.errors
        assert form.user is None
#
    def test_validate_invalid_password(self, user, db):
        user.set_password('example')
        db.session.add(user)
        db.session.commit()
    #    user.save()
        form = LoginForm(username=user.user_name, password='wrongpassword')
        assert form.validate() is False
        assert 'Invalid password' in form.password.errors
#
    def test_validate_inactive_user(self, user, db):
        user.active = False
        user.set_password('example')
        db.session.add(user)
        db.session.commit()
    #    user.save()
        # Correct username and password, but user is not activated
        form = LoginForm(username=user.user_name, password='example')
        assert form.validate() is False
        assert 'User not activated' in form.username.errors

class TestChangePasswordForm:

    def test_validate_success(self, user, db):
        user.set_password('example')
        db.session.add(user)
        db.session.commit()
        form = ChangePasswordForm( 
                                  old_password='example', 
                                  password='new_password', 
                                  password2='new_password'
                                  )
        form.add_user(user)
        assert form.validate() is True

    def test_validate_invalid_old_password(self, user, db):
        user.set_password('example')
        db.session.add(user)
        db.session.commit()
        form = ChangePasswordForm( 
                                  old_password='example1', 
                                  password='new_password', 
                                  password2='new_password'
                                  )
        form.add_user(user)
        assert form.validate() is False
        assert 'Incorrect old password' in form.old_password.errors

    def test_validate_new_password_mismatch(self, user, db):
        user.set_password('example')
        db.session.add(user)
        db.session.commit()
        form = ChangePasswordForm( 
                                  old_password='example', 
                                  password='new_password', 
                                  password2='new_password1'
                                  )
        form.add_user(user)
        assert form.validate() is False
        assert 'Passwords must match' in form.password2.errors

class TestEmailForm:

    def test_validate_success(self, user, db):
        form = EmailForm(email='test@test.com')
        assert form.validate() is True

    def test_dupe_email(self, user, db):
        user.add_email('test@test.com')
        db.session.add(user)
        db.session.commit()
        form = EmailForm(email='test@test.com')
        assert form.validate() is False


