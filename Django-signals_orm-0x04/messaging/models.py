#!/usr/bin/env python3
"""Defines Message and Notification models."""
from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

# Custom manager for Message to handle unread messages
class UnreadMessagesManager(models.Manager):
    def get_queryset(self):
        # Override get_queryset to always filter for unread messages
        return super().get_queryset().filter(read=False)

    def for_receiver(self, user):
        """
        Returns unread messages for a specific receiver (user).
        """
        # Since get_queryset already filters for read=False, we just filter by receiver
        return self.filter(receiver=user).only('id', 'content', 'timestamp')

class Message(models.Model):
    """
    Represents a message sent from one user to another.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    parent_message = models.ForeignKey(
    'self',
    null=True,
    blank=True,
    related_name='replies',
    on_delete=models.CASCADE
)
    read = models.BooleanField(default=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    edited = models.BooleanField(default=False)
    objects = models.Manager() # The default manager
    unread = UnreadMessagesManager()
    
    class Meta:
        ordering = ['-timestamp']
        
    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} at {self.timestamp}"

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='histories')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for {self.message} at {self.edited_at}"


#Custom manager for Message to handle unread messages
class Notification(models.Model):
    """
    Represents a notification for a user.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='notifications')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user} about {self.message} at {self.timestamp}"