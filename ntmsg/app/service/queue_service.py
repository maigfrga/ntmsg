from flaskutils import app
from app.models import MessageQueue
from pgsqlutils.base import Session

import boto3
import uuid
import os


class BaseService(object):
    def push(self, **msg):
        raise NotImplementedError('Invalid backend')

    def pull(self, n_messages=1):
        raise NotImplementedError('Invalid backend')


class DBService(BaseService):
    def push(self, **msg):
        key = uuid.uuid4()
        # uuid type is not json serializable
        msg['uuid'] = str(key)
        obj = MessageQueue(key=key, msg=msg)
        obj.add()
        Session.commit()
        return obj.key

    def pull(self, n_messages=1):
        msg_list = []
        for obj in MessageQueue.objects.filter_by(limit=n_messages):
            msg_list.append(obj.msg)
            obj.delete()
        Session.commit()
        return msg_list


class SQSService(BaseService):
    def __init__(self):
        self.AWS_SECRET_ACCESS_KEY = None
        self.AWS_ACCESS_KEY_ID = None

        if ('AWS_SECRET_ACCESS_KEY' in
                os.environ and 'AWS_ACCESS_KEY_ID' in os.environ):

            self.AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
            self.AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']

        elif ('AWS_SECRET_ACCESS_KEY' in
                app.config and 'AWS_ACCESS_KEY_ID' in app.config):
            self.AWS_SECRET_ACCESS_KEY = app.config['AWS_SECRET_ACCESS_KEY']
            self.AWS_ACCESS_KEY_ID = app.config['AWS_ACCESS_KEY_ID']

        else:
            raise ValueError('invalid aws credentials')

        if 'AWS_REGION' not in app.config:
            raise ValueError('invalid aws region')
        else:
            self.queue = boto3.client(
                'sqs', region_name=app.config['AWS_REGION'])

        if 'SQS_URL' not in app.config:
            raise ValueError('invalid sqs url')

    def push(self, **msg):
        key = uuid.uuid4()

        # uuid type is not json serializable
        msg['uuid'] = str(key)

        self.queue.send_message(
            QueueUrl=app.config['SQS_URL'],
            MessageBody=msg)
        return key
