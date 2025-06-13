from django.shortcuts import render
from api.models import DiscordInvite
from django.utils.timezone import now
from datetime import timedelta


# Create your views here.
def linktree(request):
    cutoff = now() - timedelta(hours=72)
    invite = (
        DiscordInvite.objects.filter(created_at__gte=cutoff)
        .order_by("-created_at")
        .first()
    )
    return render(request, "linktree/index.html", {"invite": invite})
