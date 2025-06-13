from datetime import timedelta
from django.utils import timezone
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ApiKey, DiscordInvite
from .permissions import HasValidAppKey
from .serializers import QuestionSerializer, TestimonySerializer


class CreateQuestion(generics.CreateAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [HasValidAppKey]

    http_method_names = ["post"]

class CreateTestimony(generics.CreateAPIView):
    serializer_class = TestimonySerializer
    permission_classes = [HasValidAppKey]

    http_method_names = ["post"]

@api_view(['GET'])
def get_api_key(request):
    now = timezone.now()
    valid_keys = ApiKey.objects.filter(expires_at__gt=now).order_by('expires_at')

    if valid_keys.exists():
        key = valid_keys.first().key
    else:
        new_key = ApiKey()
        new_key.expires_at = now + timedelta(days=30)
        new_key.save()
        key = new_key.key

    return Response({"BIBLE-QNA-APP-KEY": key})

@api_view(['GET'])
def get_api_key_discord_bot(request):
    now = timezone.now()
    valid_keys = ApiKey.objects.filter(expires_at__gt=now).order_by('expires_at')

    if valid_keys.exists():
        key = valid_keys[2].key
    else:
        new_key = ApiKey()
        new_key.expires_at = now + timedelta(days=30)
        new_key.save()
        key = new_key.key

    return Response({"DISCORD-BOT-APP-KEY": key})

@api_view(["POST"])
def update_invite(request):
    api_key = request.headers.get("X-API-KEY")
    if not api_key:
        return Response({"detail": "Missing API key"}, status=400)

    now = timezone.now()
    if not ApiKey.objects.filter(key=api_key, expires_at__gt=now).exists():
        return Response({"detail": "Unauthorized"}, status=401)

    url = request.data.get("url")
    if not url:
        return Response({"detail": "Missing 'url'"}, status=400)

    # Optional: only store the latest invite
    DiscordInvite.objects.all().delete()
    invite = DiscordInvite.objects.create(url=url)

    return Response({"detail": "Invite stored", "id": invite.id}, status=201)