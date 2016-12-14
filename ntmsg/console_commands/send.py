from app.service import QueueService

import argparse
import json


def run(**kwargs):
    description = 'sending a message from the queue'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        '--settings', help='config file path', default='config.test')

    parser.add_argument(
        '--n_messages', help='message to be sent', default=1)

    args, extra_params = parser.parse_known_args()
    service = QueueService()
    result = service.send()
    print(json.dumps(result))
