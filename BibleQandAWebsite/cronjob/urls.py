from django.urls import path
from .views import expired_questions_cleanup

urlpatterns = [
    path('cleanup/', expired_questions_cleanup, name='cleanup_questions'),
]