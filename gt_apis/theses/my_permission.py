from django.db.models import Q
from rest_framework import permissions

from theses.models import SinhVien


class KLTNPermissionUser(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return (super().has_permission(request, view) and
                (request.user.groups.all().values_list('name', flat=True)
                .filter(name="giáo vụ").exists() or request.user.is_superuser))
        # return False


class SinhVienPermissionUser(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if SinhVien.objects.filter(id=request.user.id).exists():
            # Check if the user is a "sinh_vien" and has a KLTN object
            try:
                kltn = request.user.kltn_set.first()
                return kltn is not None
            except:
                return False
        else:
            # For non-"sinh_vien" users, keep the original permission logic
            return False