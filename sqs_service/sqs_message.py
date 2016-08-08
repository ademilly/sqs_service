class SQSMessage(object):
    """Simple python wrapper class around SQS.Message"""

    def __init__(self, message):
        """Initialize object

        Keyword argument:
        message (SQS.Message) -- message to be wrapped
        """

        self.sqs_message = message

    def body(self):

        return self.sqs_message.body

    def delete(self):

        return self.sqs_message.delete()

    def get_attribute(self, attribute_name, attribute_type='StringValue'):
        """Return value of attribute attribute_name of message

        Keyword arguments:
        attribute_name (string) -- name of the message attribute
        attribute_type (string) -- type of the message attribute
            cf boto3 documentation for types
        """

        return self.sqs_message.message_attributes \
            .get(attribute_name) \
            .get(attribute_type)
