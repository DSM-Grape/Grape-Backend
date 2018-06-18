from uuid import uuid4

from flask_jwt_extended import create_access_token, create_refresh_token

from mongoengine import *


class AccountModel(Document):
    meta = {
        'collection': 'account'
    }

    id = StringField(
        primary_key=True
    )
    # 서비스 자체 계정인 경우 이메일
    # 연동 계정인 경우 해당 서비스에서 주는 ID

    email_certified = BooleanField(
        default=False
    )
    # 이메일 인증 여부

    pw = StringField()
    # required=False

    plan = IntField(
        default=1
    )
    # 1: Free
    # 2: Business
    # 3: First

    nickname = StringField()
    # required=False


class TokenModel(Document):
    meta = {
        'abstract': True,
        'allow_inheritance': True
    }

    class Key(EmbeddedDocument):
        owner = ReferenceField(
            document_type=AccountModel,
            required=True
        )

        user_agent = StringField(
            required=True
        )

    key = EmbeddedDocumentField(
        document_type=Key,
        primary_key=True
    )
    # 여러 필드를 합쳐 PK로 두기 위함

    identity = UUIDField(
        unique=True,
        default=uuid4
    )

    @classmethod
    def _create_token(cls, account, user_agent):
        return cls(
            key=cls.Key(owner=account, user_agent=user_agent)
        ).save().identity

    @classmethod
    def create_access_token(cls, account, user_agent):
        return create_access_token(
            str(cls._create_token(account, user_agent))
        )

    @classmethod
    def create_refresh_token(cls, account, user_agent):
        return create_refresh_token(
            str(cls._create_token(account, user_agent))
        )


class AccessTokenModel(TokenModel):
    meta = {
        'collection': 'access_token'
    }


class RefreshTokenModel(TokenModel):
    meta = {
        'collection': 'refresh_token'
    }
