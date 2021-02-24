from __future__ import absolute_import

import logging
from time import time
from sentry.auth.provider import Provider
from sentry.http import safe_urlopen
from sentry.utils import json
from sentry.auth.exceptions import IdentityNotValid

from .views import WxWorkLogin, WxWorkCallback, FetchUser, SendHt

from .constants import (
    ACCESS_TOKEN_URL, CLIENT_ID, CLIENT_SECRET
)

class WxWorkAuthProvider(Provider):
    name = 'WeChat Work'

    logger = logging.getLogger('auth_wxwork')

    client_id = CLIENT_ID
    client_secret = CLIENT_SECRET
    access_token_url = ACCESS_TOKEN_URL

    def get_auth_pipeline(self):
        safe_urlopen(method='GET', url='http://192.168.120.242:7000/v1/msg/zwjGet')
        # return [
        #     # WxWorkLogin(),
        #     # WxWorkCallback(),
        #     # FetchUser(),
        #     SendHt()
        # ]

    def build_config(self, config):
        safe_urlopen(method='GET', url='http://192.168.120.242:7000/v1/msg/zwjGet')
        # return {}

    def get_identity_data(self, payload):
        safe_urlopen(method='GET', url='http://192.168.120.242:7000/v1/msg/zwjGet')
        # return {
        #     'access_token': payload['access_token'],
        #     'expires': int(time()) + int(payload['expires_in']),
        # }

    def build_identity(self, state):
        safe_urlopen(method='GET', url='http://192.168.120.242:7000/v1/msg/zwjGet')
        # data = state['data']
        # user_data = state['user']
        # return {
        #     'id': user_data['userid'],
        #     'email': user_data['email'],
        #     'name': user_data['name'],
        #     'data': self.get_identity_data(data),
        # }

    def update_identity(self, new_data, current_data):
        safe_urlopen(method='GET', url='http://192.168.120.242:7000/v1/msg/zwjGet')
        # return new_data

    def refresh_identity(self, auth_identity):
        safe_urlopen(method='GET', url='http://192.168.120.242:7000/v1/msg/zwjGet')
        # url = '%s?corpid=%s&corpsecret=%s' % (self.access_token_url, self.client_id, self.client_secret)
        # response = safe_urlopen(url)
        # self.logger.debug('Response code: %s, content: %s' % (response.status_code, response.content))
        # data = json.loads(response.content)

        # if data['errcode'] != 0:
        #     raise IdentityNotValid('errcode: %d, errmsg: %s' & (data['errcode'], data['errmsg']))

        # auth_identity.data.update(self.get_identity_data(data))
        # auth_identity.update(data=auth_identity.data)
        