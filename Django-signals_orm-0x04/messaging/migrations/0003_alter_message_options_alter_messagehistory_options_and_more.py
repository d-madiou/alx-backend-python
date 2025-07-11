# Generated by Django 5.2.3 on 2025-06-14 18:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0002_message_edited_messagehistory'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-timestamp']},
        ),
        migrations.AlterModelOptions(
            name='messagehistory',
            options={'ordering': ['-edited_at']},
        ),
        migrations.AlterModelOptions(
            name='notification',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddField(
            model_name='message',
            name='parent_message',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='messaging.message'),
        ),
        migrations.AddField(
            model_name='message',
            name='read',
            field=models.BooleanField(default=False),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['receiver', 'read'], name='messaging_m_receive_6da6d1_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['sender', 'read'], name='messaging_m_sender__12c98b_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['parent_message'], name='messaging_m_parent__e699d7_idx'),
        ),
        migrations.AddIndex(
            model_name='notification',
            index=models.Index(fields=['user', 'is_read'], name='messaging_n_user_id_bd7d88_idx'),
        ),
    ]
