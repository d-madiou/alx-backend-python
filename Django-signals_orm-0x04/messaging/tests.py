#!/usr/bin/env python3
"""Unit tests for Messaging signals."""
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, Notification

User = get_user_model()

class SignalTestCase(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username="sender", password="pass")
        self.receiver = User.objects.create_user(username="receiver", password="pass")

    def test_notification_created_on_message(self):
        self.assertEqual(Notification.objects.count(), 0)
        msg = Message.objects.create(sender=self.sender, receiver=self.receiver, content="Hello!")
        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.receiver)
        self.assertEqual(notification.message, msg)
