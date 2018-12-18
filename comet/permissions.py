from rest_framework import permissions
from events.models import Event
from accounts.models import CustomUser

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed
        if type(obj) == Event:
            return obj.author == request.user
        if type(obj == CustomUser):
            return obj == request.user




