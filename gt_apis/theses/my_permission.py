from django.db.models import Q
from rest_framework import permissions


class CommentPermissionUser(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, comment):
        return super().has_permission(request, view) and request.user == comment.user


class KLTNPermissionUser(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return (super().has_permission(request, view) and
                (request.user.groups.all().values_list('name', flat=True)
                .filter(name="giáo vụ").exists() or request.user.is_superuser))
        # return False