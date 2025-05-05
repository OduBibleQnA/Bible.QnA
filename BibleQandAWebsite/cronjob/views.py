import os
from django.http import JsonResponse, HttpResponseForbidden
from django.utils.timezone import now
from form.models import Question
from django.db.models import Q

def run_question_cleanup(request):
    key = request.GET.get("key")
    expected_key = os.getenv("CRON_SECRET_KEY")
    
    if key != expected_key:
        return HttpResponseForbidden("Forbidden")

    today = now().date()
    expired_questions = Question.objects.filter(
        Q(marked_date__lt=today) | Q(answered=True),
        archived=False
    )
    count = expired_questions.update(archived=True)
    return JsonResponse({"archived": count})
