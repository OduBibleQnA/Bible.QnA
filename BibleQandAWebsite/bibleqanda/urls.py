from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("form.urls")),
    path("leaders/", include("leaders.urls")),
    path("auth/", include("register.urls")),
    path("cron/", include("cronjob.urls")),
    path("bibleqna/api/", include("api.urls")),
]
