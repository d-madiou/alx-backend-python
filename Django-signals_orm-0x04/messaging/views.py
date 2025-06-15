#!/usr/bin/env python3
from django.shortcuts import render
from django.contrib.auth import logout
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch

from .models import Message, Notification, Conversation
from .managers import UnreadMessagesManager

@cache_page(60) # Cache this view for 60 seconds
@login_required # Ensures only logged-in users can access
def message_list(request):
    # This view now displays all messages (useful for admin or overview)
    messages = Message.objects.select_related('sender', 'conversation') \
                             .prefetch_related('replies') \
                             .order_by('-timestamp')
    return render(request, 'messaging/messages.html', {'messages': messages})

@login_required
def threaded_conversation_view(request, conversation_id):
    conversation = Conversation.objects.get(pk=conversation_id)
    # Ensure the current user is a participant in the conversation
    if request.user not in conversation.participants.all():
        # You might want to raise a 403 Forbidden or redirect
        return render(request, 'messaging/access_denied.html', {'message': 'You are not a participant in this conversation.'}, status=403)

    messages = Message.objects.filter(conversation=conversation, parent_message__isnull=True) \
        .select_related('sender', 'receiver') \
        .prefetch_related(
            Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver').order_by('timestamp'))
        ).order_by('timestamp')

    return render(request, 'messaging/threaded_conversation.html', {
        'conversation': conversation,
        'messages': messages
    })

@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user).select_related('message', 'message__sender')
    return render(request, 'messaging/notifications.html', {'notifications': notifications})

@login_required
def unread_messages(request):
    # Use the custom manager's method to get unread messages for the current user
    # The .only() optimization is handled within the UnreadMessagesManager's for_receiver method
    messages = Message.unread.unread_for_user(request.user)
    return render(request, 'messaging/unread_messages.html', {'unread_messages': messages})

@login_required # Added login_required for this sensitive action
def sent_messages(request):
    """
    Displays messages sent by the current user.
    """
    messages = Message.objects.filter(sender=request.user).only('id', 'content', 'timestamp', 'receiver') \
                             .order_by('-timestamp')
    return render(request, 'messaging/sent_messages.html', {'sent_messages': messages})

@login_required
def delete_user(request):
    user = request.user
    logout(request) # Log out the user before deleting
    user.delete()
    return render(request, 'messaging/account_deleted.html', {
        'user': user,
        'message': 'Your account has been deleted successfully.'
    })