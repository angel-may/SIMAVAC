# 📁 backend/biologicos_app/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Permite lectura (GET, HEAD, OPTIONS) a usuarios autenticados.
    Requiere rol Administrador (o superuser/staff) para crear, editar o eliminar.
    """
    def has_permission(self, request, view):
        # ✅ Si solo quiere leer, basta con estar autenticado
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated

        # ✅ Si quiere modificar datos, debe ser admin o superusuario
        if not (request.user and request.user.is_authenticated):
            return False

        # 🧩 Ajusta a tu modelo de roles personalizado
        user_role = getattr(request.user, "rol", None)
        if isinstance(user_role, str):
            return user_role.lower() == "administrador"
        elif hasattr(user_role, "nombre"):
            return user_role.nombre.lower() == "administrador"

        # Fallback a superuser/staff
        return getattr(request.user, "is_staff", False) or getattr(request.user, "is_superuser", False)
