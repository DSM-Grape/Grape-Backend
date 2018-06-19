import copy
import jwt

from datetime import datetime
from unittest import TestCase as TC
from uuid import UUID

import pymongo
from flask import Response
from redis import Redis

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

        self.redis_client = Redis(**self.app.config['REDIS_SETTINGS'])

        self.client = self.app.test_client()
        self.today = datetime.now().strftime('%Y-%m-%d')
        self.now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.token_regex = '([\w\-\_]+\.){2}[\w\-\_]+'

        super(TCBase, self).__init__(*args, **kwargs)

    def _create_fake_account(self):
        self.primary_user_pw = 'primary'

        self.primary_user = AccountModel(
            id='mingyu.planb@gmail.com',
            pw=generate_password_hash(self.primary_user_pw),
            email_certified=True,
            nickname='primary'
        ).save()

        self.fb_user = AccountModel(
            id='100006735372513',
            email_certified=False,
            nickname='secondary'
        ).save()

    def _generate_tokens(self):
        with self.app.app_context():
            self.primary_user_access_token = 'JWT ' + AccessTokenModel.create_access_token(self.primary_user, 'TEST')
            self.primary_user_refresh_token = 'JWT ' + RefreshTokenModel.create_refresh_token(self.primary_user, 'TEST')
            self.fb_user_access_token = 'JWT ' + AccessTokenModel.create_access_token(self.fb_user, 'TEST')
            self.fb_user_refresh_token = 'JWT ' + RefreshTokenModel.create_refresh_token(self.fb_user, 'TEST')

    def setUp(self):
        self._create_fake_account()
        self._generate_tokens()

    def tearDown(self):
        self.mongo_client.drop_database(self.db_name)
        self.redis_client.flushall()

    def request(self, method, target_url_rule, token=None, *args, **kwargs) -> Response:
        return method(
            target_url_rule,
            headers={'Authorization': token or self.primary_user_access_token},
            *args,
            **kwargs
        )

    def assert_response_tokens(self, data):
        self.assertIn('accessToken', data)
        self.assertIn('refreshToken', data)

        access_token = data['accessToken']
        refresh_token = data['refreshToken']

        self.assertRegex(access_token, self.token_regex)
        self.assertRegex(refresh_token, self.token_regex)

        # (4) 데이터베이스 확인
        self.assertTrue(AccessTokenModel.objects(identity=UUID(jwt.decode(access_token, self.app.secret_key)['identity'])))
        self.assertTrue(RefreshTokenModel.objects(identity=UUID(jwt.decode(refresh_token, self.app.secret_key)['identity'])))
