import hmac
import os

from rest_framework.permissions import BasePermission


class IsAPIUser(BasePermission):
    def has_permission(self, request, view):
        api_key = request.headers.get("API-Key")
        return api_key and hmac.compare_digest(api_key, os.environ["MEETINGS_API_SECRET"])
