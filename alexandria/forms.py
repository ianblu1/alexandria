# -*- coding: utf-8 -*-
from flask_wtf import Form 
from wtforms import TextField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

#from flask_login import current_user

from alexandria.models.users import User


class LoginForm(Form):
    username = TextField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            print('no initial validation')
            return False

        self.user = User.query.get(self.username.data)
        if not self.user:
            self.username.errors.append('Unknown username')
            print('Unknown username')
            return False
        if not self.user.check_password(self.password.data):
            self.password.errors.append('Invalid password')
            print('Invalid password')
            return False
        if not self.user.active:
            self.username.errors.append('User not activated')
            print('User not activated')
            return False
        return True

class RegisterForm(Form):
    username = TextField('Username', validators=[DataRequired(), Length(min=3, max=25)])
    first_name = TextField('first_name', validators=[DataRequired(), Length(min=3, max=25)])
    last_name = TextField('last_name', validators=[DataRequired(), Length(min=3, max=25)])
    email = TextField('Email', validators=[DataRequired(), Email(), Length(min=6, max=40)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=40)])
    confirm = PasswordField('Verify password', [DataRequired(), EqualTo('password', message='Passwords must match')])

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        
        # user = User.query.filter_by(username=self.username.data).first()
        # if user:
        #     self.username.errors.append("Username already registered")
        #     return False
        # user = User.query.filter_by(email=self.email.data).first()
        # if user:
        #     self.email.errors.append("Email already registered")
        #     return False
        return True

class EmailForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    email_submit = SubmitField('Add')

    def __init__(self, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super(EmailForm, self).validate()
        if not initial_validation:
            return False

        return True


class ChangePasswordForm(Form):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm New Password',
                              validators=[DataRequired(), EqualTo('password', message='Passwords must match')])

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.user = None

    def add_user(self, user):
        self.user = user

    def validate(self):
        initial_validation = super(ChangePasswordForm, self).validate()
        if not initial_validation:
            return False

        #self.user = current_user
        if not self.user.check_password(self.old_password.data):
            self.old_password.errors.append('Incorrect old password')
            print('Incorrect old password')
            return False

        return True

class ChangeUsernameForm(Form):
    password = PasswordField('Your Password', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    username2 = StringField('Confirm Username',
                            validators=[DataRequired(), EqualTo('username', message='Usernames must match')])

    def __init__(self, *args, **kwargs):
        super(ChangeUsernameForm, self).__init__(*args, **kwargs)
        self.user = None

    def add_user(self, user):
        self.user = user

    def validate(self):
        initial_validation = super(ChangeUsernameForm, self).validate()
        if not initial_validation:
            return False

        #self.user = current_user
        if not self.user.check_password(self.password.data):
            self.old_password.errors.append('Invalid password')
            print('Incorrect old password')
            return False

        user = User.query.filter_by(user_name=self.username.data).first()
        if user:
            self.username.errors.append("Username already registered")
            return False


        return True

