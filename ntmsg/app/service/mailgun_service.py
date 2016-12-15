from flaskutils import app
from requests.auth import HTTPBasicAuth

import requests
import os


class MailGunService(object):
    def __init__(self):
        if 'MAILGUN_API_KEY' in app.config:
            self.api_key = app.config['MAILGUN_API_KEY']
        elif 'MAILGUN_API_KEY' in os.environ:
            self.api_key = os.environ['MAILGUN_API_KEY']
        else:
            raise ValueError('invalid mailgun credentials')

        if 'MAILGUN_DOMAIN_NAME' in app.config:
            self.domain = app.config['MAILGUN_DOMAIN_NAME']
        else:
            raise ValueError('invalid mailgun domain name')

        self.url = 'https://api.mailgun.net/v3/{}/messages'.format(
            self.domain
        )
        self.headers = {
        }

    def send(self, msg):

        auth = HTTPBasicAuth('api', self.api_key)
        requests.post(
            self.url, params=msg, auth=auth)
        return msg['uuid']
