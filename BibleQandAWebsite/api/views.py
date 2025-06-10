from datetime import timedelta
from django.utils import timezone
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ApiKey
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
