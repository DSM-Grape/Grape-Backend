from uuid import UUID

from flask import Blueprint, abort, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_refresh_token_required
from flask_restful import Api
from flasgger import swag_from

from app.models.account import TokenModel, AccessTokenModel, RefreshTokenModel
from app.views import BaseResource

api = Api(Blueprint(__name__, __name__))
api.prefix = ''


@api.resource('/refresh')
class Refresh(BaseResource):
    @jwt_refresh_token_required
    def post(self):
        """
        Access token refresh
        """
        try:
            token = RefreshTokenModel.objects(identity=UUID(get_jwt_identity())).first()

            if not token:
                abort(401)

            return {
                'accessToken': create_access_token(
                    str(AccessTokenModel(
                        key=TokenModel.Key(owner=token.key.owner, user_agent=request.headers['USER_AGENT'])
                    ))
                )
            }
        except ValueError:
            abort(422)
