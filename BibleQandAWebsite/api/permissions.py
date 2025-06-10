from rest_framework.permissions import BasePermission
from django.conf import settings

class HasValidAppKey(BasePermission):
    def has_permission(self, request, view):
        app_key = request.headers.get("X-APP-KEY")
        return app_key == settings.APP_SECRET_KEY
