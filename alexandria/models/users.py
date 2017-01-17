from alexandria.extensions import db, bcrypt
from sqlalchemy.dialects.postgresql import TSVECTOR, BYTEA
import datetime as dt
import hashlib as hl

from alexandria.models.documentlinks import DocumentLink

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Text, unique=True, nullable=False)
    #email = db.Column(db.Text, unique=True, nullable=False)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    user_name = db.Column(db.Text, primary_key=True, nullable=False)
    password = db.Column(BYTEA, nullable=False)
    authenticated = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean)
    is_admin = db.Column(db.Boolean)
    is_deleted = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime)
    emails = db.relationship('UserEmail', backref=db.backref('User'),
                             lazy='dynamic')
    documents = db.relationship('DocumentLink', backref='User',
                                lazy='dynamic')

    def __init__(self,email,user_name, first_name, last_name, password, is_admin=False, active=True):
        self.emails = [UserEmail(email, user_name)]
        self.first_name = first_name
        self.last_name = last_name
        self.user_name = user_name
        self.active = active
        self.is_admin = is_admin
        self.created_at = dt.datetime.now()
        self.id = hl.md5(str("_".join([email, user_name, first_name, last_name])).encode('utf-8')  ).hexdigest()
        self.is_deleted = False
        if password:
            self.set_password(password)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        return bcrypt.check_password_hash(self.password, value)

    def add_email(self, email):
        self.emails.append(UserEmail(email, self.user_name))

    #@property
    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.user_name

    @property
    def is_active(self):
        return self.active

    @property
    def is_authenticated(self):
        return self.authenticated

    @property
    def is_anonymous(self):
        """we don't allow anonymous users"""
        return False

class UserEmail(db.Model):
    __tablename__='user_emails'

    id = db.Column(db.BigInteger, primary_key=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    user_name = db.Column(db.Text, db.ForeignKey('users.user_name'))
    is_deleted = db.Column(db.Boolean)

    def __init__(self, email, user_name):
        self.email = email
        self.user_name = user_name
        self.is_deleted = False

