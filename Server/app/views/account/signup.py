import random
from string import ascii_uppercase, digits

from flask import Blueprint, Response, abort, current_app, request
from flask_mail import Message
from flask_restful import Api
from flasgger import swag_from

from werkzeug.security import generate_password_hash

from app.models.account import AccountModel
from app.views import BaseResource, json_required

api = Api(Blueprint(__name__, __name__))
api.prefix = ''


def generate_email_certification_code(email):
    """
    전달된 email에 12자리의 인증 코드를 매핑하여 반환합니다. 인증 코드는 하루 동안만 유효합니다.
    """
    redis_client = current_app.config['REDIS_CLIENT']

    while True:
        code = ''.join(random.choice(ascii_uppercase + digits) for _ in range(12))

        if not redis_client.exists(code):
            redis_client.set(code, email, ex=3600 * 24)
            # 하루동안 유지

            return code


def send_certify_mail(target_email: str):
    """
    전달된 target_email로 인증 이메일을 전송합니다.
    """
    mail_client = current_app.config['MAIL_CLIENT']

    code = generate_email_certification_code(target_email)

    msg = Message('Please verify user email', sender=current_app.config['MAIL_USERNAME'], recipients=[target_email])
    msg.html = '<a href="http://{0}:{1}/certify/{2}">인증하기</a>'.format(
        current_app.config['REPRESENTATIVE_HOST'] or current_app.config['HOST'],
        current_app.config['PORT'] if not current_app.testing else 80,
        code
    )

    mail_client.send(msg)


@api.resource('/email/check/<email>')
class CheckEmail(BaseResource):
    def get(self, email):
        """
        이메일 중복체크
        """
        return Response('', 409 if AccountModel.objects(id=email) else 200)


@api.resource('/is-certified/email/<email>')
class CheckIsCertifiedEmail(BaseResource):
    def get(self, email):
        """
        인증된 이메일인지 확인
        """
        account = AccountModel.objects(id=email).first()

        return Response('', 200 if account and account.email_certified else 401)


@api.resource('/signup')
class Signup(BaseResource):
    @json_required({'email': str, 'pw': str})
    def post(self):
        """
        회원가입
        """
        payload = request.json

        email = payload['email']
        pw = payload['pw']

        if AccountModel.objects(email=email):
            abort(409)

        send_certify_mail(email)

        AccountModel(
            email=email,
            pw=generate_password_hash(pw)
        ).save()

        return Response('', 201)


@api.resource('/email-resend/<email>')
class EmailResend(BaseResource):
    def get(self, email):
        """
        이메일 재전송
        """
        account = AccountModel.objects(email=email).first()

        if not account:
            return Response('', 204)

        if account.email_certified:
            return Response('', 208)

        send_certify_mail(email)

        return Response('', 200)


@api.resource('/certify/<code>')
class EmailCertify(BaseResource):
    def get(self, code):
        """
        이메일 인증 URL
        """
        redis_client = current_app.config['REDIS_CLIENT']

        email = redis_client.get(code)

        if not email:
            # 유효하지 않은 코드
            abort(404)

        account = AccountModel.objects(id=email).first()

        if not account:
            abort(401)

        account.update(email_certified=True)

        redis_client.delete(code)

        return Response('Welcome!', 200)
