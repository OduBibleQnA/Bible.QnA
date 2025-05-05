from django.urls import path
from .views import run_question_cleanup

urlpatterns = [
    path('cleanup/', run_question_cleanup, name='cleanup_questions'),
]