# [Requests](https://github.com/kennethreitz/requests) for [GitHub OAuth](http://developer.github.com/v3/oauth/) Helpers

## Offline/Non-Web Application Flow

Set environment ```GH_USER``` and ```GH_PASSWORD``` which will be used only once at
```Authorization``` init.

### Create a new authorization

List of [available scopes](http://developer.github.com/v3/oauth/#scopes) and [other authorization parameters](http://developer.github.com/v3/oauth/#create-a-new-authorization)

```python
from requests_github_oauth import Authorization

github_authorization = Authorization(scopes=['user'], note='just testing')
github_authorization.put()
github_authorization.data['token']
'ACCESS_TOKEN'
github_authorization.data['id']
'AUTHORIZATION_ID'
```

### If you have created an authorization already:

Build [Requests](http://python-requests.org) ```AuthorizedClient``` for the [GitHub API](http://developer.github.com/)

```python
from requests_github_oauth import Authorization, AuthorizedClient

github_authorization = Authorization('AUTHORIZATION_ID')
api = AuthorizedClient(github_authorization)

# use api client helper to make api calls
r = api.get('/user')
assert r.status_code == 200
assert 'login' in r.json()
```
