"""Requests github-oauth helpers for offline/non-web application flow

Uses $ENV <GH_USER>, <GH_PASSWORD> once at Authorization init. Then uses
token-based authenticated client. Example:

    >>> github_authorization = Authorization(850974)
    >>> client = AuthorizedClient(github_authorization)

    >>> r = client.get('/user')
    >>> print r.status_code
    >>> print r.json()
"""
import os
import json

import requests
from oauthlib.oauth2.draft25 import tokens
from requests.auth import AuthBase

__version__ = '0.0.2'
__about__ = 'requests github-oauth helpers'
__all__ = [
    'Authorization', 'AuthorizedClient',

    # extra
    'BaseAuthenticationBearer',
    'HeaderAuthenticationBearer',
    'URIAuthenticationBearer']


API_URL = 'https://api.github.com'


class Authorization(object):
    """OAuth GitHub offline mode Authorizations.

    Set env ``GH_USER``, ``GH_PASSWORD`` or pass them as `basic_auth` tuple:
        >>> Authorization(basic_auth=('LOGIN', 'PASS'))

    Create new authorization:
        >>> authorization = Authorization(scopes=['user'])
        >>> authorization.put()
        >>> authorization.data['token']
        ACCESS_TOKEN
        >>> authorization.data[id]
        AUTHORIZATION_ID

    Or use existing by id:
        >>> authorization = Authorization('AUTHORIZATION_ID')
    """
    @staticmethod
    def _assert_status(response, expected_code):
        msg = 'Got %s (expected %s)\n%s' % (
            response.status_code, expected_code, response.content)
        assert response.status_code == expected_code, msg

    def __init__(self, authorization_id=None, basic_auth=None, **kwargs):
        if not basic_auth:
            basic_auth = (os.environ['GH_USER'], os.environ['GH_PASSWORD'])
        self.basic_auth = basic_auth

        if authorization_id:
            url = '%s/authorizations/%s' % (API_URL, authorization_id)
            r = requests.get(url, auth=self.basic_auth)
            self._assert_status(r, 200)
            self.data = r.json()
        else:
            self.data = kwargs

    @property
    def is_saved(self):
        return self.data.get('id') is not None

    def put(self):
        if self.is_saved:
            r = requests.patch(
                self.data['url'],
                data=json.dumps(self.data),
                auth=self.basic_auth)
            self._assert_status(r, 200)
        else:
            r = requests.post(
                API_URL + '/authorizations',
                data=json.dumps(self.data),
                auth=self.basic_auth)
            self._assert_status(r, 201)
            self.data = r.json()

    def delete(self):
        if not self.is_saved:
            raise Exception('Not saved?')
        r = requests.delete(self.data['url'], auth=self.basic_auth)
        self._assert_status(r, 204)
        del self.data['id']


class BaseAuthenticationBearer(AuthBase):
    """Base class to build AuthenticationBearer types

    __call__ must get implemented according to AuthBase.__call__ documentation.
    """
    def __init__(self, github_authorization):
        super(BaseAuthenticationBearer, self).__init__()
        assert github_authorization.is_saved
        self.token = github_authorization.data['token']


class HeaderAuthenticationBearer(BaseAuthenticationBearer):
    """
    Authenticate using the "Authorization: bearer TOKEN" header. Setup:
        >>> github_authorization = Authorization('AUTHORIZATION_ID')
        >>> requests_auth = HeaderAuthenticationBearer(github_authorization)
        >>> client = requests.session(auth=requests_auth)

    Then make client requests:
        >>> client.get('/user').status_code
    """
    def __call__(self, r):
        r.headers = tokens.prepare_bearer_headers(self.token, r.headers)
        return r


class URIAuthenticationBearer(BaseAuthenticationBearer):
    """
    Authenticate using the "&token=TOKEN" URI param. Setup:
        >>> github_authorization = Authorization('AUTHORIZATION_ID')
        >>> requests_auth = URIAuthenticationBearer(github_authorization)
        >>> client = requests.session(auth=requests_auth)

    Then make client requests:
        >>> client.get('/user').status_code
    """
    def __call__(self, r):
        r.url = tokens.prepare_bearer_uri(self.token, r.url)
        return r


class AuthorizedClient(requests.Session):
    """
    Friendly shorthand to get authenticated client:
        >>> github_authorization = Authorization('AUTHORIZATION_ID')
        >>> client = AuthorizedClient(github_authorization)

    Then make client requests:
        >>> client.get('/user').status_code
        200
    """
    def __init__(self, github_authorization,
                 bearer_cls=HeaderAuthenticationBearer, **kwargs):
        super(AuthorizedClient, self).__init__(**kwargs)
        self.auth = bearer_cls(github_authorization)

    def request(self, method, url, *args, **kwargs):
        """Make the URL setup"""
        assert url.startswith('/'), 'Expected /API_URL:%s' % url
        api_url = API_URL + url
        return super(AuthorizedClient, self).request(
            method, api_url, *args, **kwargs)
