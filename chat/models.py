from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey(get_user_model(), verbose_name='sender', on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(get_user_model(), verbose_name='receiver', on_delete=models.CASCADE, related_name='receiver')
    content = models.TextField()
    chat_id = models.CharField(max_length=127)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.sender} -> {self.receiver}"
    