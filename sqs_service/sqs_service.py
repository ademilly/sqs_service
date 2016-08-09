# -*- coding: utf-8 -*-

import boto3
from collections import deque

from sqs_message import SQSMessage


class SQSService(object):
    """Simple SQS queue messaging class
    Assumes credentials are presented before usage via environment variables

    Expected set environment variables:
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - AWS_DEFAULT_REGION
    - AWS_SESSION_TOKEN for IAM roles
    - AWS_SECURITY_TOKEN for IAM roles
    """
    sqs = boto3.resource('sqs')

    def __init__(self, queue_name):
        """Initialize queue object"""

        self.queue = self.sqs.get_queue_by_name(QueueName=queue_name)
        self.messages = deque()

    def listen(self, for_how_many=1, with_attributes=[]):
        """Listen to the queue

        Keyword arguments:
        for_how_many (int) -- number of message to get at once
        with_attributes [str] -- expected attributes in the message
        """

        for message in self.queue.receive_messages(
            MessageAttributeNames=with_attributes
        ):
            if message.message_attributes is not None:
                self.messages.append(
                    message
                )

        return self

    def has_got_messages(self):
        """Checks if messages are on deque"""

        return len(self.messages) > 0

    def purge_queue(self):
        """Purge queue of all messages"""

        return self.queue.purge()

    def get_first_message(self):
        """Pop first message"""

        return SQSMessage(self.messages.popleft())

    def get_last_message(self):
        """Pop last message"""

        return SQSMessage(self.messages.pop())

    def send(self, body='Hello', attributes={}):
        """Send message to the queue

        Keyword arguments:
        body (str) -- message body
        attributes ({key: str}) -- message attributes, should be a python dict
        """

        return self.queue.send_message(
            MessageBody=body,
            MessageAttributes=self.format_attribute(attributes)
        )

    @staticmethod
    def format_attribute(attributes):
        """Return a SQS message ready dict for message attributes"""

        attr_dict = {}
        for key in attributes:
            attr_dict[key] = {
                'StringValue': attributes[key],
                'DataType': 'String'
            }

        return attr_dict
