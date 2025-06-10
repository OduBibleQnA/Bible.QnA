from django.core.management.base import BaseCommand
from api.models import ApiKey
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = "Rotate API keys: delete expired and generate new ones if count too low"

    def handle(self, *args, **kwargs):
        now = timezone.now()
        expired_keys = ApiKey.objects.filter(expires_at__lte=now)
        expired_count = expired_keys.count()
        expired_keys.delete()
        self.stdout.write(f"Deleted {expired_count} expired API keys.")

        MIN_KEYS = 5  # minimum keys you want active
        current_count = ApiKey.objects.count()
        keys_to_create = max(0, MIN_KEYS - current_count)

        for _ in range(keys_to_create):
            new_key = ApiKey()
            new_key.expires_at = now + timedelta(days=30)  # set expiry
            new_key.save()
            self.stdout.write(f"Created new API key: {new_key.key}")