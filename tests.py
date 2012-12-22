import unittest2 as unittest
from requests_github_oauth import Authorization, AuthorizedClient


class TestFoo(unittest.TestCase):
    def test_AuthorizedClient(self):
        github_authorization = Authorization(850974)
        client = AuthorizedClient(github_authorization)

        r = client.get('https://api.github.com/user/repos')
        self.assertEqual(200, r.status_code)


if __name__ == '__main__':
    unittest.main()
