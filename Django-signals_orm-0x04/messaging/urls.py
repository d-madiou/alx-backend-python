from django.urls import path
from . import views

urlpatterns = [
    path('messages/', views.message_list, name='message_list'),
    path('notifications/', views.notification_list, name='notification_list'),
    path('delete_user/', views.delete_user, name='delete_user'),
    path('unread_messages/', views.unread_messages, name='unread_messages'),
    path('conversations/<uuid:conversation_id>/', views.threaded_conversation_view, name='threaded_conversation'),
    # Add more URL patterns as needed
]
