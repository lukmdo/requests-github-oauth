# [Requests](https://github.com/kennethreitz/requests) for [GitHub OAuth](http://developer.github.com/v3/oauth/) Helpers

```python

from requests_github_oauth import Authorization, AuthorizedClient

github_authorization = Authorization(850974)
client = AuthorizedClient(github_authorization)

# ...life goes on
r = client.get('https://api.github.com/user/repos')
pp([r.status_code, r.json])

```