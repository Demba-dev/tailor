from django.db import models
from django.contrib.auth.models import User
from apps.personnel.models import Personnel

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', verbose_name="Expéditeur")
    recipient = models.ForeignKey(Personnel, on_delete=models.CASCADE, related_name='received_messages', verbose_name="Destinataire")
    subject = models.CharField(max_length=255, verbose_name="Sujet")
    body = models.TextField(verbose_name="Message")
    is_read = models.BooleanField(default=False, verbose_name="Lu")
    is_archived = models.BooleanField(default=False, verbose_name="Archivé")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Envoyé le")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return f"{self.subject} (De: {self.sender.username})"
