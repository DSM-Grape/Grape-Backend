from tests.views import TCBase


class TestEmailDuplicationCheck(TCBase):
    """
    이메일 중복 체크를 테스트합니다.
    """

    def __init__(self, *args, **kwargs):
        super(TestEmailDuplicationCheck, self).__init__(*args, **kwargs)

        self.method = self.client.get
        self.target_uri = '/email/check/{}'

    def setUp(self):
        super(TestEmailDuplicationCheck, self).setUp()

        # ---

        self._request = lambda *, email=self.primary_user.id: self.request(
            self.method,
            self.target_uri.format(email),
        )

    def test_check_with_existing_email(self):
        self.assertEqual(self._request().status_code, 409)

    def test_check_with_non_existing_email(self):
        self.assertEqual(self._request(email='a').status_code, 200)


class TestEmailCertifiedCheck(TCBase):
    """
    이메일 인증 여부를 테스트합니다.
    """

    def __init__(self, *args, **kwargs):
        super(TestEmailCertifiedCheck, self).__init__(*args, **kwargs)

        self.method = self.client.get
        self.target_uri = '/is-certified/email/{}'

    def setUp(self):
        super(TestEmailCertifiedCheck, self).setUp()

        # ---

        self._request = lambda *, email=self.primary_user.id: self.request(
            self.method,
            self.target_uri.format(email),
        )

    def test_check_with_email_certified_account(self):
        self.assertEqual(self._request().status_code, 200)

    def test_check_with_email_unauthorized_account(self):
        self.primary_user.update(
            email_certified=False
        )

        self.assertEqual(self._request().status_code, 401)
