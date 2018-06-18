from flask import Blueprint, Response, abort, g, request
from flask_restful import Api
from flasgger import swag_from

from app.models.account import AccountModel
from app.views import BaseResource, auth_required, json_required

api = Api(Blueprint(__name__, __name__))
api.prefix = '/info'


@api.resource('/initialize')
class InitializeInfo(BaseResource):
    @json_required({'id': str, 'nickname': str})
    def post(self):
        payload = request.json

        id = payload['id']
        nickname = payload['nickname']

        account = AccountModel.objects(id=id).first()

        if not account:
            return Response('', 204)

        if AccountModel.objects(nickname=nickname):
            abort(409)

        account.update(nickname=account.nickname or nickname)
        # 덮어쓰기 방지

        return Response('', 200)
