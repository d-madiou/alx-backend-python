#!/usr/bin/env python3
"""Views for conversations and messages API."""

from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from typing import Type


class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for handling conversations."""
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        """Filter conversations to only show those where user is a participant."""
        return self.queryset.filter(participants=self.request.user)

    def perform_create(self, serializer):
        """Create conversation and add creator as participant."""
        conversation = serializer.save()
        conversation.participants.add(self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    """ViewSet for handling messages."""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.OrderingFilter]
    ordering = ['-timestamp']

    def get_queryset(self):
        """Filter messages to only show those in conversations where user is a participant."""
        return self.queryset.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        """Create message with current user as sender."""
        serializer.save(sender=self.request.user)