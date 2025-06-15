#!/usr/bin/env python3
"""
Custom model managers for the Messaging app.
"""

from django.db import models


class UnreadMessagesManager(models.Manager):
    """
    Manager to retrieve unread messages for a specific user.
    Usage:
        Message.unread.for_user(user)
    """

    def for_user(self, user):
        return self.get_queryset().filter(receiver=user, read=False).only('id', 'content', 'timestamp')
