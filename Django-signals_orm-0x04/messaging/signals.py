#!/usr/bin/env python3
"""Signal to create notifications on new messages."""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification

@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    """
    Automatically create a notification when a new message is sent.
    """
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)
