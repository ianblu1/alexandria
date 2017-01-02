# -*- coding: utf-8 -*-
from factory import Sequence, PostGenerationMethodCall
from factory.alchemy import SQLAlchemyModelFactory

from alexandria.models.users import User
from alexandria.extensions import db


class BaseFactory(SQLAlchemyModelFactory):

    class Meta:
        abstract = True
        sqlalchemy_session = db.session


class UserFactory(BaseFactory):
    user_name = Sequence(lambda n: "user{0}".format(n))
    first_name = Sequence(lambda n: "fn{0}".format(n))
    last_name = Sequence(lambda n: "ln{0}".format(n))
    email = Sequence(lambda n: "user{0}@example.com".format(n))
    #password = PostGenerationMethodCall('set_password', 'example')
    password = 'example'
    active = True

    class Meta:
        model = User
