import os
from django.http import JsonResponse, HttpResponseForbidden
from django.utils.timezone import now
from form.models import Question, Testimony
from api.models import ApiKey, DiscordInvite
from django.db.models import Q
from datetime import timedelta

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

def rotate_api_keys(request):
    key = request.GET.get("key")
    expected_key = os.getenv("CRON_SECRET_KEY")

    if key != expected_key:
        return HttpResponseForbidden("Forbidden")

    current_time = now()
    expired_keys = ApiKey.objects.filter(expires_at__lte=current_time)
    expired_count = expired_keys.count()
    expired_keys.delete()

    MIN_KEYS = 5
    summary = {}
    
    for source in ["app", "bot"]:
        valid_keys = ApiKey.objects.filter(source=source, expires_at__gt=current_time)
        current_count = valid_keys.count()
        keys_to_create = max(0, MIN_KEYS - current_count)

        for _ in range(keys_to_create):
            new_key = ApiKey(source=source)
            new_key.save()

        summary[source] = {
            "valid_keys": ApiKey.objects.filter(source=source, expires_at__gt=current_time).count(),
            "created": keys_to_create,
        }

    return JsonResponse({
        "expired_deleted": expired_count,
        "per_source": summary,
        "total_keys": ApiKey.objects.count(),
    })


def rotate_invites(request):
    key = request.GET.get("key")
    expected_key = os.getenv("CRON_SECRET_KEY")

    if key != expected_key:
        return HttpResponseForbidden("Forbidden")

    current_time = now()
    expiration_cutoff = current_time - timedelta(days=3)  # 72 hours

    expired_invites = DiscordInvite.objects.filter(created_at__lte=expiration_cutoff)
    expired_count = expired_invites.count()
    expired_invites.delete()

    return JsonResponse({
        "expired_deleted": expired_count,
        "remaining": DiscordInvite.objects.count()
    })