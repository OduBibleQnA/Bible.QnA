from django.urls import path
from . import views

urlpatterns = [path("", views.linktree, name="linktree")]
