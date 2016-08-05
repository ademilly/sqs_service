# -*- coding: utf-8 -*-

import boto3
from collections import deque

"""Simple SQS queue messaging class
Assumes credentials are presented before usage via environment variables

Expected set environment variables:
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_DEFAULT_REGION
- AWS_SESSION_TOKEN for IAM roles
- AWS_SECURITY_TOKEN for IAM roles
"""


class SQSService(object):
    """Initialize sqs resource to be available for every class object"""
    sqs = boto3.resource('sqs')

    def __init__(self, queue_name):
        """Initialize queue object"""

        self.queue = self.sqs.get_queue_by_name(QueueName=queue_name)
        self.messages = deque()

    def listen(self, for_how_many=1, with_attributes=[]):
        """Listen to the queue

        Keyword arguments:
        for_how_many -- number of message to get at once
        with_attributes -- expected attributes in the message, [string]
        """

        self.messages.extend(
            self.queue.receive_messages(
                MessageAttributeNames=with_attributes
            )
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

        return self.messages.popleft()

    def get_last_message(self):
        """Pop last message"""

        return self.messages.pop()

    def send(self, body='Hello', attributes={}):
        """Send message to the queue

        Keyword arguments:
        body -- message body
        attributes -- message attributes, should be a python dict {key: string}
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

    @staticmethod
    def get_attribute(message, attribute_name):
        """Return value of attribute attribute_name of message"""

        return message.message_attributes \
            .get(attribute_name) \
            .get('StringValue')
