import json

import requests

from flask import Blueprint, Response, abort, request
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import Api
from flasgger import swag_from

from werkzeug.security import check_password_hash

from app.models.account import AccountModel, TokenModel, AccessTokenModel, RefreshTokenModel
from app.views import BaseResource, json_required

api = Api(Blueprint(__name__, __name__))
api.prefix = ''


@api.resource('/auth')
class Auth(BaseResource):
    @json_required({'email': str, 'pw': str})
    def post(self):
        """
        로그인
        """
        payload = request.json

        email = payload['email']
        pw = payload['pw']

        account = AccountModel.objects(id=email).first()

        if not account:
            abort(401)
        else:
            if check_password_hash(account.pw, pw):
                if not account.email_certified:
                    abort(403)

                if not account.nickname:
                    return Response('', 204)

                return {
                    'accessToken': create_access_token(
                        str(AccessTokenModel(
                            key=TokenModel.Key(owner=account, user_agent=request.headers['USER_AGENT'])
                        ).save().identity)
                    ),
                    'refreshToken': create_refresh_token(
                        str(RefreshTokenModel(
                            key=TokenModel.Key(owner=account, user_agent=request.headers['USER_AGENT'])
                        ).save().identity)
                    )
                }
            else:
                abort(401)

