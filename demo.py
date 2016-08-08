# -*- coding: utf-8 -*-

import time

import sqs_service

"""Usage:
python demo.py

Expected set environment variables:
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_DEFAULT_REGION
- AWS_SESSION_TOKEN for IAM roles
- AWS_SECURITY_TOKEN for IAM roles

Send 'Hello World' to queue 'TEST', listen to the queue and
print first message received
"""


def run():

    sqs_svc = sqs_service.SQSService(queue_name='TEST')
    sqs_svc.send(body='Hello World', attributes={
        'MessageType': 'Greeting'
    })

    t_end = time.time() + 30
    while time.time() < t_end:

        sqs_svc.listen(for_how_many=1, with_attributes=['MessageType'])

        if sqs_svc.has_got_messages():
            first_message = sqs_svc.get_first_message()
            print 'Message received:', first_message.body()
            print 'Message is a', first_message.get_attribute('MessageType')
            first_message.delete()

if __name__ == '__main__':

    run()
