from rest_framework.permissions import BasePermission

def in_group(user, name: str) -> bool:
    return user.is_authenticated and user.groups.filter(name=name).exists()

class IsAdminRole(BasePermission):
    def has_permission(self, request, view): return in_group(request.user, 'admin')

class IsEnfermeraRole(BasePermission):
    def has_permission(self, request, view): return in_group(request.user, 'enfermera')

class IsDoctorRole(BasePermission):
    def has_permission(self, request, view): return in_group(request.user, 'doctor')

class IsTutorRole(BasePermission):
    def has_permission(self, request, view): return in_group(request.user, 'tutor')
