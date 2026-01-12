from django.db import models
from django.contrib.auth.models import User
from .base import TimeStampedModel

class Notification(TimeStampedModel):
    TYPES = (
        ('info', 'Information'),
        ('success', 'Succès'),
        ('warning', 'Avertissement'),
        ('danger', 'Urgent'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=20, choices=TYPES, default='info')
    title = models.CharField(max_length=255)
    message = models.TextField()
    link = models.CharField(max_length=255, blank=True, null=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.username}"
