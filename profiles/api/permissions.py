from rest_framework.permissions import BasePermission

class IsOwnerPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        return obj.user == request.user