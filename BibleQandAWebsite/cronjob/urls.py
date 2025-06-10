from django.urls import path
from .views import run_question_cleanup, rotate_api_keys

urlpatterns = [
    path('cleanup/', run_question_cleanup, name='cleanup_questions'),
    path('rotate-keys/', rotate_api_keys, name='rotate_keys'),
    
]