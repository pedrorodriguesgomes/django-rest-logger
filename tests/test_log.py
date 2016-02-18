#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-rest-logger
------------

Tests for `django-rest-logger` logger module.
"""
import logging

from django.test import TestCase

from djangorestlogger import settings
from djangorestlogger.logger import DjangoRestLogger


class MockLoggingHandler(logging.Handler):
    """
    Mock logging handler to check for expected logs.

    Messages are available from an instance's ``messages`` dict, in order,
    indexed by a lowercase log level string (e.g., 'debug', 'info', etc.).

    From: http://www.pythonbackend.com/topic/1243032268
    """

    def __init__(self, *args, **kwargs):
        self.messages = {'debug': [], 'info': [], 'warning': [], 'error': [],
                         'critical': []}
        super(MockLoggingHandler, self).__init__(*args, **kwargs)

    def emit(self, record):
        "Store a message from ``record`` in the instance's ``messages`` dict."
        self.acquire()
        try:
            self.messages[record.levelname.lower()].append(record.getMessage())
        finally:
            self.release()

    def reset(self):
        self.acquire()
        try:
            for message_list in self.messages.values():
                message_list.clear()
        finally:
            self.release()


class TestDjangorestlogger(TestCase):
    def setUp(self):
        self.logging_handler = MockLoggingHandler(level='DEBUG')
        self.log = logging.getLogger(settings.DEFAULT_LOGGER)
        self.log.addHandler(self.logging_handler)

    def test_warning(self):
        DjangoRestLogger.log_warning(message='a warning message',
                                     details={'item': 'details'})
        self.assertEqual(self.logging_handler.messages['warning'],
                         ['a warning message'])

    def test_error(self):
        DjangoRestLogger.log_error(message='an error message',
                                   details={},
                                   status_code=400)
        self.assertEqual(self.logging_handler.messages['error'],
                         ['an error message'])

    def test_exception(self):
        try:
            a = []
            a[0]
        except:
            DjangoRestLogger.log_exception()
            self.assertEqual(self.logging_handler.messages['error'],
                             ['list index out of range'])
