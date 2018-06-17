from uuid import uuid4

from mongoengine import *


class AccountModel(Document):
    meta = {
        'collection': 'account'
    }

    id = StringField(
        primary_key=True
    )

    pw = StringField()
    # required=False

    plan = IntField(
        default=1
    )
    # 1: Free
    # 2: Business
    # 3: First

    email = StringField()
    # required=False

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


class AccessTokenModel(Document):
    meta = {
        'collection': 'access_token'
    }


class RefreshTokenModel(Document):
    meta = {
        'collection': 'refresh_token'
    }

    pw_snapshot = StringField()