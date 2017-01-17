# -*- coding: utf-8 -*-
from flask_wtf import Form 
from wtforms import TextField, PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length

#from flask_login import current_user

from alexandria.models.users import User, UserEmail
from alexandria.models.documentlinks import DocumentLink


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

        email = UserEmail.query.filter_by(email=self.email.data).first()
        if email:
            self.email.errors.append('Email Already Registered')
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

class NewDocumentForm(Form):
    url = StringField('url', validators=[DataRequired()])
    title = StringField('title', validators=[DataRequired()])
    tags = StringField('tags', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(NewDocumentForm, self).__init__(*args, **kwargs)
        self.user = None

    def add_user(self, user):
        self.user = user

    def validate(self):
        initial_validation = super(NewDocumentForm, self).validate()
        if not initial_validation:
            return False

        document = DocumentLink.query.filter_by(url=self.url.data).first()
        if document:
            if document.creating_user == self.user.user_name:
                self.url.errors.append("Document Already Exists.")
                return False

        return True

class SearchForm(Form):
    search = StringField('Search the docs', validators=[DataRequired()])


