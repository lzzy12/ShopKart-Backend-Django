from rest_framework import permissions


class IsCreatorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user == obj.creator)


class IsUnAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.auth is None
