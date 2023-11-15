from django.db import models

import accounts.models


# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey(accounts.models.CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(accounts.models.CustomUser, related_name='received_messages', on_delete=models.CASCADE)
    message_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
