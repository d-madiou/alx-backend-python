from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import View
from typing import Optional

from .models import Conversation

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    """
    def has_object_permission(self, request: Request, view: View, obj, Conversation) -> bool:
        if not request.user.is_authenticated:
            return False
        if isinstance(obj, Conversation):
            return obj.participants.filter(user_id=request.user.user_id).exists()
        return False