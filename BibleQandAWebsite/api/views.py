from datetime import timedelta
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
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
    valid_keys = ApiKey.objects.filter(source='app', expires_at__gt=now).order_by('created')

    if valid_keys.count() >= 5:
        key = valid_keys.first().key  # reuse oldest valid key
    else:
        new_key = ApiKey(source='app')
        new_key.save()
        key = new_key.key

    return Response({"BIBLE-QNA-APP-KEY": key})

@csrf_exempt
@api_view(["POST"])
def update_invite(request):
    api_key = request.headers.get("X-API-KEY")
    if not api_key:
        return Response({"detail": "Missing API key"}, status=400)

    now = timezone.now()
    key_qs = ApiKey.objects.filter(key=api_key)

    if not key_qs.exists():
        return Response({"detail": "Invalid API key"}, status=401)

    key = key_qs.first()
    if key.expires_at <= now:
        return Response({"detail": "API key expired"}, status=403)  # Use 403 for expired but valid keys

    url = request.data.get("url")
    if not url or not isinstance(url, str):
        return Response({"detail": "Missing or invalid 'url'"}, status=400)

    DiscordInvite.objects.all().delete()
    invite = DiscordInvite.objects.create(url=url)

    return Response({
        "detail": "Invite stored",
        "id": invite.id,
        "url": invite.url
    }, status=201)
