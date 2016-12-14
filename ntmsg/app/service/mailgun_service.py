from flaskutils import app

import os

class MailGunService(object):
    def __init__(self):
        if 'MAILGUN_API_KEY' in app.config:
            self.api_key = app.config['MAILGUN_API_KEY']
        elif 'MAILGUN_API_KEY' in os.environ:
            self.api_key = os.environ['MAILGUN_API_KEY']
        else:
            raise ValueError('invalid mailgun credentials')

        self.headers = {
        }


    def send(self, msg):
        payload = {
            'from': msg['from'],
            'subject': msg['subject'],
            'text': msg['text']
        }

        for recipient in msg['to']:
            m = payload.copy()
            m['to'] = recipient
            print(m)
        return msg['uuid']
