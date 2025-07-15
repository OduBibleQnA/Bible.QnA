from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("form.urls")),
    path("leaders/", include("leaders.urls")),
    path("auth/", include("register.urls")),
    path("cron/", include("cronjob.urls")),
    path("bibleqna/api/", include("api.urls")),
    path("linktree/", include("linktree.urls")),
]

from django.conf import settings
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)