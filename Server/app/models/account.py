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

