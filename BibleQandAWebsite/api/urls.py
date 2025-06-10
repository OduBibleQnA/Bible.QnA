from django.urls import path
from api.views import CreateQuestion, CreateTestimony


urlpatterns = [
    path("new/key/", CreateQuestion.as_view(), name="question_create"),
    path("new/question/", CreateQuestion.as_view(), name="question_create"),
    path("new/testimony/", CreateTestimony.as_view(), name="testimony_create"),
]