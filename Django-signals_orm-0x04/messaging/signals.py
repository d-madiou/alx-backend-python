#!/usr/bin/env python3
"""Signal to create notifications on new messages."""
import contextlib
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, MessageHistory, Notification, User

@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    """
    Automatically create a notification when a new message is sent.
    """
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)
@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.id:
        with contextlib.suppress(Message.DoesNotExist):
            old_message = Message.objects.get(id=instance.id)
            if old_message.content != instance.content:
                MessageHistory.objects.create(
                    message=instance,
                    old_content=old_message.content
                )
                instance.edited = True
@receiver(post_delete, sender=User)
def delete_all(sender, instance, **kwargs):
    """
    Automatically delete notifications when a message is deleted.
    Ensure that foreign key constraints are respected during the deletion process by using CASCADE or custom signal logic.
    """
    Notification.objects.filter(message=instance).delete()
    MessageHistory.objects.filter(message=instance).delete()
    Message.objects.filter(id=instance.id).delete()