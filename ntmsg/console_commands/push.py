from app.service import QueueService

import argparse
import json


def run(**kwargs):
    description = 'Pushing a message to the queue'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        '--settings', help='config file path', default='config.test')

    parser.add_argument(
        '--msg', help='message to be sent', required=True)

    args, extra_params = parser.parse_known_args()
    msg = json.loads(args.msg)
    service = QueueService()
    uuid = service.push(**msg)
    print(uuid)
