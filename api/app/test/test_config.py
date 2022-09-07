# import the necessary package

from flask import current_app
from flask_testing import TestCase
from manage import app
from app.main.config import mysql_local_base, BASE_DIR
import unittest
import os

class TestDevelopmentConfig(TestCase):
    """
        to be sure that the environment is working well use this couple of tests for it
    """
    def create_app(self):
        app.config.from_object('app.main.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        """* test for dev env :"""
        self.assertFalse(app.config['SECRET_KEY'] is 'secret_key')
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == mysql_local_base
        )

class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('app.main.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        """* test for test env :"""
        self.assertFalse(app.config['SECRET_KEY'] is 'test_secret_key')
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///' + os.path.join(BASE_DIR, 'eproc_api_test.db')
        )
class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object('app.main.config.ProductionConfig')
        return app

    def test_app_is_production(self):
        """* test for product env :"""
        self.assertTrue(app.config['DEBUG'] is False)

if __name__ == '__main__':
    if __name__ == '__main__':
        unittest()
