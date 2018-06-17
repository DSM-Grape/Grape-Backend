from flask import Blueprint, Response, abort, current_app, request
from flask_restful import Api
from flasgger import swag_from

from app.models.account import AccountModel
from app.views import BaseResource, json_required

api = Api(Blueprint(__name__, __name__))
api.prefix = ''


@api.resource('/email/check/<email>')
class CheckEmail(BaseResource):
    def get(self, email):
        """
        이메일 중복체크
        """
        return Response('', 409 if AccountModel.objects(email=email) else 200)

