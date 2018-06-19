from tests.views import TCBase


class TestInitializeInfo(TCBase):
    """
    기본 정보 업로드를 테스트합니다.
    """

    def __init__(self, *args, **kwargs):
        super(TestInitializeInfo, self).__init__(*args, **kwargs)

        self.method = self.client.post
        self.target_uri = '/info/initialize'

        self.new_nickname = 'test'

    def setUp(self):
        super(TestInitializeInfo, self).setUp()

        # ---

        self.primary_user.update(
            nickname=None
        )

        self._request = lambda *, id=self.primary_user.id, nickname=self.new_nickname: self.request(
            self.method,
            self.target_uri,
            json={
                'id': id,
                'nickname': nickname
            }
        )

    def test_initialize_success(self):
        # (1) 정보 업로드
        resp = self._request()

        # (2) status code 200
        self.assertEqual(resp.status_code, 200)

        # (3) 데이터베이스 확인
        self.primary_user.reload()

        self.assertEqual(self.primary_user.nickname, self.new_nickname)

    def test_initialize_with_unknown_id(self):
        self.assertEqual(self._request(id='1').status_code, 204)

    def test_initialize_with_already_initialized_account_id(self):
        self.primary_user.update(
            nickname=self.new_nickname
        )

        self.assertEqual(self._request().status_code, 208)

    def test_initialize_with_duplicated_nickname(self):
        self.assertEqual(self._request(nickname=self.fb_user.nickname).status_code, 409)
