from cryptography.fernet import Fernet
from django.conf import settings
from rest_framework import serializers
from .models import Question, Testimony

cipher = Fernet(settings.ENCRYPTION_KEY)

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            "id",
            "first_name",
            "question",
        ]

    def create(self, validated_data):
        question = Question.objects.create(**validated_data)
        return question


class TestimonySerializer(serializers.ModelSerializer):
    contact_detail = serializers.CharField(write_only=True)

    class Meta:
        model = Testimony
        fields = [
            "name",
            "shortened_testimony",
            "on_camera",
            "contact_method",
            "contact_detail",  # write-only virtual field
        ]

    def validate_contact_detail(self, value):
        if not value:
            raise serializers.ValidationError("Contact detail must be included")
        return value

    def create(self, validated_data):
        # Extract contact_detail from POST data
        contact_detail = validated_data.pop("contact_detail")

        # Create instance without saving yet
        instance = Testimony(**validated_data)

        # Use model's encryption method
        instance.set_contact_detail(contact_detail)

        # Save to DB
        instance.save()
        return instance
