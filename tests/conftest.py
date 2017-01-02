# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""
import os

import pytest
from webtest import TestApp

#from ese.settings import TestConfig
from alexandria.app import create_app
from alexandria.extensions import db as _db

from .factories import UserFactory


@pytest.yield_fixture(scope='function')
def app():
    _app = create_app('test')
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope='function')
def testapp(app):
    """A Webtest app."""
    return TestApp(app)


@pytest.yield_fixture(scope='function')
def db(app):
    _db.app = app
    with app.app_context():
        _db.session.remove()
        _db.drop_all()
        _db.create_all()

    yield _db

    _db.session.remove()
    _db.drop_all()

    ## This dispose() call is needed to avoid the DB locking
    ## between tests.
    ## Thanks to:
    ## http://stackoverflow.com/a/18293157/2066849
    ## See also: 
    ## http://stackoverflow.com/questions/28487950
    _db.get_engine(_db.app).dispose()


@pytest.fixture
def user(db):
    user = UserFactory(password='myprecious')
    #db.session.add(user)
    db.session.commit()
    return user

