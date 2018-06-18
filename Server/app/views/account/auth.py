import requests

from flask import Blueprint, Response, abort, request
from flask_restful import Api
from flasgger import swag_from

from werkzeug.security import check_password_hash

from app.models.account import AccountModel, AccessTokenModel, RefreshTokenModel
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
                    'accessToken': AccessTokenModel.create_access_token(account, request.headers['USER_AGENT']),
                    'refreshToken': RefreshTokenModel.create_refresh_token(account, request.headers['USER_AGENT'])
                }
            else:
                abort(401)


@api.resource('/auth/facebook')
class FacebookAuth(BaseResource):
    FB_GRAPH_API_URL = 'https://graph.facebook.com/v2.6/{}?access_token=1925974487664670|D-wibfbjkOaHtINm_cwUSBx38k8'

    def get_nickname_through_fb_id(self, fb_id):
        resp = requests.get(self.FB_GRAPH_API_URL.format(fb_id))
        # 페이스북 graph api를 이용해 사용자 데이터 조회

        data = resp.json()

        return False if 'error' in data else data['name']

    @json_required({'id': str})
    def post(self):
        """
        페이스북 계정 로그인
        """
        payload = request.json

        id = payload['id']

        account = AccountModel.objects(id=id).first()

        if not account:
            # 사용자가 미존재, 회원가입을 시켜줌
            name = self.get_nickname_through_fb_id(id)

            if name:
                account = AccountModel(
                    id=id,
                    nickname=name
                ).save()
            else:
                abort(401)

        return {
            'accessToken': AccessTokenModel.create_access_token(account, request.headers['USER_AGENT']),
            'refreshToken': RefreshTokenModel.create_refresh_token(account, request.headers['USER_AGENT'])
        }
