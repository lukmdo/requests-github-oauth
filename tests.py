import unittest2 as unittest
from requests_github_oauth import Authorization, AuthorizedClient


class TestFoo(unittest.TestCase):
    def test_AuthorizedClient(self):
        github_authorization = Authorization(850974)
        client = AuthorizedClient(github_authorization)

        r = client.get('/user')
        self.assertEqual(r.status_code, 200)
        self.assertIn('login', r.json())

if __name__ == '__main__':
    unittest.main()
