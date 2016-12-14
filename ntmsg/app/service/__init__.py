from flaskutils import app

from .queue_service import DBService, SQSService
from .mailgun_service import MailGunService  # noqa


class QueueService():
    """
    Instanciate proper Queue service based in configuration
    """
    def __init__(self):
        if 'POSTGRES' == app.config['QUEUE_BAKEND']:
            self.backend = DBService()
        elif 'AWS_SQS' == app.config['QUEUE_BAKEND']:
            self.backend = SQSService()
        else:
            raise NotImplementedError('Invalid backend')
        self.mailgun = MailGunService()


    def push(self, **msg):
        return self.backend.push(**msg)

    def pull(self, n_messages=1):
        return self.backend.pull(n_messages=n_messages)

    def send(self, n_messages=1, msg=None):
        msg_uuids = []
        if msg is None:
            for msg in self.pull(n_messages=n_messages):
                msg_uuids.append(self.mailgun.send(msg))
        return msg_uuids
