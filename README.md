# [Requests](https://github.com/kennethreitz/requests) for [GitHub OAuth](http://developer.github.com/v3/oauth/) Helpers

## Offline-Style (Non-Web Application Flow)

Fill```AUTHORIZATION_ID```, ```LOGIN``` and ```PASSWORD``` like in example:

```python

from requests_github_oauth import Authorization, AuthorizedClient

github_authorization = Authorization(AUTHORIZATION_ID, basic_auth=('LOGIN', 'PASSWORD'))
client = AuthorizedClient(github_authorization)

# ...life goes on
r = client.get('https://api.github.com/user/repos')
pp([r.status_code, r.json])

```
