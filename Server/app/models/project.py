from mongoengine import *

from app.models.account import AccountModel


class ProjectModel(Document):
    meta = {
        'collection': 'project'
    }

    name = StringField(
        required=True
    )

    apidoc = DictField()
    # default={}

    owner = ReferenceField(
        document_type=AccountModel,
        required=True
    )

    members = ListField(
        ReferenceField(
            document_type=AccountModel,
            required=True
        )
    )
    # default=[]
