#!/usr/bin/env python3
"""Admin interface for Messaging app."""
from django.contrib import admin
from .models import Message, Notification

admin.site.register(Message)
admin.site.register(Notification)
