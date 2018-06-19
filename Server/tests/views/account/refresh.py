from uuid import uuid4

from flask_jwt_extended import create_refresh_token

from tests.views import TCBase


class TestRefresh(TCBase):
    """
    JWT 토큰 refresh를 테스트합니다.
    """

    def __init__(self, *args, **kwargs):
        super(TestRefresh, self).__init__(*args, **kwargs)

        self.method = self.client.post
        self.target_uri = '/refresh'

    def setUp(self):
        super(TestRefresh, self).setUp()

        # ---

        self._request = lambda *, token=None: self.request(
            self.method,
            self.target_uri,
            token
        )

    def test_refresh_success(self):
        # (1) refresh
        resp = self._request(token=self.primary_user_refresh_token)

        # (2) status code 200
        self.assertEqual(resp.status_code, 200)

        # (3) response data
        data = resp.json

        self.assertIn('accessToken', data)

        access_token = data['accessToken']

        self.assertIsInstance(access_token, str)

        self.assertRegex(data['accessToken'], self.token_regex)

    def test_refresh_with_unknown_identity(self):
        # (1) 유효하지 않은(존재하지 않는) refresh token을 통해 refresh
        with self.app.app_context():
            resp = self._request(token='JWT {}'.format(create_refresh_token(str(uuid4()))))

        # (2) status code 401
        self.assertEqual(resp.status_code, 401)

    def test_refresh_with_invalid_identity(self):
        # (1) 유효하지 않은 identity 값이 들어간 refresh token을 통해 refresh
        with self.app.app_context():
            resp = self._request(token='JWT {}'.format(create_refresh_token('123')))

        # (2) status code 422
        self.assertEqual(resp.status_code, 422)
