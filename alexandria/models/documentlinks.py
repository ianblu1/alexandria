from alexandria.extensions import db, bcrypt
from sqlalchemy.dialects.postgresql import TSVECTOR, BYTEA
import datetime as dt
import hashlib as hl

documentlink_tags = db.Table('documentlink_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
    db.Column('documentlink_id', db.Integer, db.ForeignKey('documentlinks.id')),
    db.PrimaryKeyConstraint('documentlink_id', 'tag_id')
)

class DocumentLink(db.Model):
    __tablename__ = 'documentlinks'
    __table_args__ = (
        db.Index('ix_documentlinks', 'document_vector', postgresql_using="gin"),
        )

    id = db.Column(db.BigInteger, primary_key=True)
    url = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    slug = db.Column(db.Text)
    title = db.Column(db.Text)
    document_vector = db.Column(TSVECTOR)
    date_added = db.Column(db.DateTime)
    creating_user = db.Column(db.Text, db.ForeignKey('users.user_name'))
    tags = db.relationship('Tag', secondary=documentlink_tags,
        backref=db.backref('documentlinks', lazy='dynamic'))

    def __init__(self, user, url, title, description, slug):
        self.creating_user = user.user_name
        self.url = url
        self.description = description
        self.title = title
        self.slug = slug
        self.date_added = dt.datetime.now()
        

class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.BigInteger, primary_key=True)
    tag = db.Column(db.Text)
    date_added = db.Column(db.DateTime)

    def __init__(self, tag):
        self.tag = tag
        self.date_added = dt.datetime.now()

