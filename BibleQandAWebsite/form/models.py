from django.db import models
from .utils.encryption import encrypt_contact_detail, decrypt_contact_detail
from django.utils import timezone

class Question(models.Model):
    first_name = models.CharField(max_length=15, blank=True, null=True)
    question = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    # Staff fields
    answered = models.BooleanField(default=False)
    answer_medium = models.CharField(
        max_length=20,
        choices=[('podcast', 'Podcast'), ('bible_study', 'Bible Study')],
        blank=True,
        null=True
    )
    answer_date = models.DateField(blank=True, null=True)
    archived = models.BooleanField(default=False)

    def is_expired(self):
        return self.answer_date and self.answer_date < timezone.now().date()

    def __str__(self):
        return f"{self.first_name or 'Anonymous'}: {self.question[:50]}"



class Testimony(models.Model):
    name = models.CharField(max_length=100)
    shortened_testimony = models.TextField()
    on_camera = models.BooleanField()
    contact_method = models.CharField(max_length=20, choices=[
        ('instagram', 'Instagram'),
        ('phone', 'Phone'),
        ('email', 'Email')
    ])
    encrypted_contact_detail = models.TextField()
    approved = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)

    def set_contact_detail(self, plain_text):
        self.encrypted_contact_detail = encrypt_contact_detail(plain_text)

    def get_contact_detail(self):
        return decrypt_contact_detail(self.encrypted_contact_detail)

    def __str__(self):
        return f"{self.name} ({self.contact_method})"
