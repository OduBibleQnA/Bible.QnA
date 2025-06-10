from django.db import models
from django.utils import timezone
import secrets
from datetime import timedelta

class ApiKey(models.Model):
    key = models.CharField(max_length=40, unique=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = secrets.token_hex(20)  # 40 hex chars
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(days=30)  # default expiry 30 days
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() >= self.expires_at

    def __str__(self):
        return f"API Key {self.key} (expires {self.expires_at})"
