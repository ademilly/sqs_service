#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='sqs_service',
    version='0.1',
    description='Python SQS Wrapper',
    author='Aurélien Demilly',
    author_email='demilly.aurelien@gmail.com',
    url='https://github.com/ademilly/sqs_service',
    license='MIT',
    packages=['sqs_service'],
    install_requires=[
        'boto3>=1.4.0',
    ]
)
