"""
Example

>>> github_authorization = Authorization(850974)
>>> client = AuthorizedClient(github_authorization)

>>> r = client.get('https://api.github.com/user/repos')
>>> print r.status_code
>>> print r.json
"""

import os
import json

import requests
from requests.auth import AuthBase

__version__ = '0.0.1'
__about__ = 'requests github-oauth helpers'
__all__ = ['Authorization', 'OAuth2', 'AuthorizedClient']


class Authorization(object):
    """
    OAuth GitHub offline mode Authorizations.

    >>> from requests_github_oauth import Authorization

    Set env `GH_USER`, `GH_PASSWORD` or pass them as `basic_auth` tuple:
    >>> Authorization(basic_auth=('LOGIN', 'PASS'))

    Create new authorization:
    >>> authorization = Authorization(scopes=['user'], note='Open Source IT!')
    >>> authorization.put()
    >>> authorization.data['token']
    ACCESS_TOKEN
    >>> authorization.data[id]
    AUTHORIZATION_ID

    Or use existing by id:
    >>> authorization = Authorization(id=AUTHORIZATION_ID)
    """
    _URL = 'https://api.github.com/authorizations'
    requests_auth = None

    def __init__(self, id=None, basic_auth=None, scopes=None, note=None,
                 note_url=None):
        """
        :param scopes: optional any subset ['user', 'public_repo', '...']
        :param note:
        :param note_url:
        :return:
        """
        if not basic_auth:
            basic_auth = (os.environ['GH_USER'], os.environ['GH_PASSWORD'])
        self.basic_auth = basic_auth

        if id:
            r = requests.get('%s/%s' % (self._URL, id), auth=self.basic_auth)
            assert r.status_code == 200
            self.data = r.json()
        else:
            self._new_data = dict(scopes=scopes, note=note, note_url=note_url)

    @property
    def is_saved(self):
        return hasattr(self, 'data')

    def put(self):
        if self.is_saved:
            payload = dict(
                scopes=self.data.get('scopes'),
                note=self.data.get('note'),
                note_url=self.data.get('note_url'))
            r = requests.patch(self.data['url'],
                               data=json.dumps(payload),
                               auth=self.basic_auth)
            assert r.status_code == 200
        else:
            payload = self._new_data
            r = requests.post(self._URL,
                              data=json.dumps(payload),
                              auth=self.basic_auth)
            assert r.status_code == 201
            self.data = r.json


class OAuth2(AuthBase):
    """OAuth2 class for github-requests usage:

    Get/Create authorization:
    >>> github_authorization = Authorization(authorization_id=ID,
                                             basic_auth=('LOGIN', 'PASS'))

    Then:
    >>> requests_auth = OAuth2(github_authorization)
    >>> client = requests.session(auth=auth)

    Or BETTER:
    >>> client = AuthorizedClient(github_authorization)

    ... life goes on:
    >>> client.get('https://api.github.com/user/repos').status_code
    200
    """

    def __init__(self, github_authorization):
        super(OAuth2, self).__init__()
        assert github_authorization.is_saved
        self.github_authorization = github_authorization

    def __call__(self, r):
        r.prepare_url(
            r.url,
            dict(access_token=self.github_authorization.data['token']))
        return r


class AuthorizedClient(requests.Session):
    def __init__(self, github_authorization=None, requests_auth=None,
                 **kwargs):
        super(AuthorizedClient, self).__init__(**kwargs)

        if github_authorization:
            self.github_authorization = github_authorization
            self.auth = OAuth2(github_authorization)
        else:
            self.github_authorization = requests_auth.github_authorization
            self.auth = requests_aut
