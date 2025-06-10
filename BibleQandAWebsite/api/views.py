from rest_framework import generics
from .serializers import QuestionSerializer, TestimonySerializer
from .permissions import HasValidAppKey
import secrets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import APIKey


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
    new_key = secrets.token_urlsafe(32)
    APIKey.objects.create(key=new_key)
    return Response({'key': new_key})
