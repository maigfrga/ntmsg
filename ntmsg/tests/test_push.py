from flaskutils import app
from flaskutils.test import TransactionalTestCase
from app.models import MessageQueue
from app.service import QueueService, MailGunService

import pytest


MSG = {
    'uuid': '95d818b8_9bd0_11e4_a12 4_28d2447f45b8',
    'from': 'sender@email.com',
    'to': ['user1@email.com', 'user2@another.com'],
    'subject': 'test message',
    'text': 'hello world',
    'html': '<h1>Hello world</h1>',
    'reply_to': ['email1@mydomain.com', 'email2@mydomain.com']
}



class TestDBBackend(TransactionalTestCase):
    def setup(self):
        super(TestDBBackend, self).setup()

    def test_create_msg(self):
        app.config['QUEUE_BAKEND'] = 'POSTGRES'
        assert 0 == MessageQueue.objects.count()
        service = QueueService()
        uuid = service.push(**MSG)
        assert 1 == MessageQueue.objects.count()
        msg_list = service.pull()

        assert msg_list[0]['uuid'] == str(uuid)


class TestSQSBackend(object):
    def test_raise_invalid_config(self):
        app.config['QUEUE_BAKEND'] = 'AWS_SQS'

        with pytest.raises(ValueError) as excinfo:
            QueueService()
            assert 'invalid aws credentials' in str(excinfo)

        app.config['AWS_SECRET_ACCESS_KEY'] = 'key'
        app.config['AWS_ACCESS_KEY_ID'] = 'access'

        if 'AWS_REGION' in app.config:
            del app.config['AWS_REGION']

        with pytest.raises(ValueError) as excinfo:
            QueueService()
            assert 'invalid aws region' in str(excinfo)


        app.config['AWS_REGION'] = 'us-west-2'

        if 'SQS_URL' in app.config:
            del app.config['SQS_URL']

        with pytest.raises(ValueError) as excinfo:
            QueueService()
            assert 'invalid sqs url' in str(excinfo)


class TestMailGunBackend(object):
    def setup(self):
        pass

    def test_error_config(self):
        if 'MAILGUN_API_KEY' in app.config:
            del app.config['MAILGUN_API_KEY']

        with pytest.raises(ValueError) as excinfo:
            MailGunService()
            assert 'invalid mailgun credentials' in str(excinfo)
