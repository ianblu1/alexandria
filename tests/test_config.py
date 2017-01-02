# -*- coding: utf-8 -*-
from alexandria.app import create_app


def test_production_config():
    app = create_app('prod')
    assert app.config['ENV'] == 'prod'
    assert app.config['DEBUG'] is False
    assert app.config['DEVELOPMENT'] is False


def test_dev_config():
    app = create_app('dev')
    assert app.config['ENV'] == 'dev'
    assert app.config['DEBUG'] is True
    assert app.config['DEVELOPMENT'] is True


def test_test_config():
    app = create_app('test')
    assert app.config['ENV'] == 'test'
    assert app.config['DEBUG'] is True
    assert app.config['DEVELOPMENT'] is True