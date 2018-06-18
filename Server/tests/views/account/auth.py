from app.models.account import AccountModel

from tests.views import TCBase


class TestAuth(TCBase):
    """
    로그인을 테스트합니다.
    """

    def __init__(self, *args, **kwargs):
        super(TestAuth, self).__init__(*args, **kwargs)

        self.method = self.client.post
        self.target_uri = '/auth'

    def setUp(self):
        super(TestAuth, self).setUp()

        # ---

        self._request = lambda *, email=self.primary_user.id, pw=self.primary_user_pw: self.request(
            self.method,
            self.target_uri,
            json={
                'email': email,
                'pw': pw
            }
        )

    def test_auth_success(self):
        # (1) 로그인
        resp = self._request()

        # (2) status code 200
        self.assertEqual(resp.status_code, 200)

        # (3) response data
        self.assert_response_tokens(resp.json)

    def test_auth_with_invalid_email_or_pw(self):
        self.assertEqual(self._request(email='q').status_code, 401)
        self.assertEqual(self._request(pw='q').status_code, 401)

    def test_auth_with_email_unauthorized_account(self):
        self.primary_user.update(
            email_certified=False
        )

        self.assertEqual(self._request().status_code, 403)

    def test_auth_with_information_not_initialized_account(self):
        self.primary_user.update(
            nickname=None
        )

        self.assertEqual(self._request().status_code, 205)


class TestFacebookAuth(TCBase):
    """
    페이스북 로그인을 테스트합니다.
    """

    def __init__(self, *args, **kwargs):
        super(TestFacebookAuth, self).__init__(*args, **kwargs)

        self.method = self.client.post
        self.target_uri = '/auth/facebook'

    def setUp(self):
        super(TestFacebookAuth, self).setUp()

        # ---

        self._request = lambda *, id=self.fb_user.id: self.request(
            self.method,
            self.target_uri,
            json={
                'id': id
            }
        )

    def test_auth_success(self):
        # (1) 로그인
        resp = self._request()

        # (2) status code 200
        self.assertEqual(resp.status_code, 200)

        # (3) response data
        self.assert_response_tokens(resp.json)

    def test_auth_with_unsigned_fb_id(self):
        unsigned_id = '100006735372113'

        # (1) 가입되지 않은 ID로 로그인
        resp = self._request(id=unsigned_id)

        # (2) status code 205
        self.assertEqual(resp.status_code, 205)

        # (3) response data
        data = resp.json

        self.assertIn('name', data)
        self.assertIsInstance(data['name'], str)

        # (4) 데이터베이스 확인
        self.assertTrue(AccountModel.objects(id=unsigned_id))

    def test_auth_with_information_not_initialized_account(self):
        self.fb_user.update(
            nickname=None
        )

        # (1) 로그인
        resp = self._request()

        # (2) status code 205
        self.assertEqual(resp.status_code, 205)

        # (3) response data
        data = resp.json

        self.assertIn('name', data)
        self.assertIsInstance(data['name'], str)

    def test_auth_failure_invalid_fb_id(self):
        self.assertEqual(self._request(id='1').status_code, 401)
