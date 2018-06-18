import copy

from datetime import datetime
from unittest import TestCase as TC

import pymongo
from flask import Response

from werkzeug.security import generate_password_hash

from app import create_app
from app.models.account import AccountModel, AccessTokenModel, RefreshTokenModel

from config.test import TestConfig


class TCBase(TC):
    def __init__(self, *args, **kwargs):
        self.app = create_app(TestConfig)

        mongo_setting = copy.copy(self.app.config['MONGODB_SETTINGS'])
        self.db_name = mongo_setting.pop('db')
        self.mongo_client = pymongo.MongoClient(**mongo_setting)

        self.client = self.app.test_client()
        self.today = datetime.now().strftime('%Y-%m-%d')
        self.now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.token_regex = '([\w\-\_]+\.){2}[\w\-\_]+'

        super(TCBase, self).__init__(*args, **kwargs)

    def _create_fake_account(self):
        self.primary_user_pw = 'primary'

        self.primary_user = AccountModel(
            id='primary',
            pw=generate_password_hash(self.primary_user_pw),
            email_certified=True,
            nickname='primary'
        ).save()

        self.fb_user = AccountModel(
            id='secondary',
            email_certified=False,
            nickname='secondary'
        ).save()

    def _generate_tokens(self):
        with self.app.app_context():
            self.primary_user_access_token = AccessTokenModel.create_access_token(self.primary_user, 'TEST')
            self.primary_user_refresh_token = RefreshTokenModel.create_refresh_token(self.primary_user, 'TEST')
            self.fb_user_access_token = AccessTokenModel.create_access_token(self.fb_user, 'TEST')
            self.fb_user_refresh_token = RefreshTokenModel.create_refresh_token(self.fb_user, 'TEST')

    def setUp(self):
        self._create_fake_account()
        self._generate_tokens()

    def tearDown(self):
        self.mongo_client.drop_database(self.db_name)

    def request(self, method, target_url_rule, token=None, *args, **kwargs) -> Response:
        return method(
            target_url_rule,
            headers={'Authorization': token or self.primary_user_access_token},
            *args,
            **kwargs
        )
