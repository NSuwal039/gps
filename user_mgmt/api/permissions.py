from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class CorrectUserOrSuperUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True

        raise PermissionDenied('Only owners or system can access this resource.')