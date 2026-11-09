from rest_framework.permissions import BasePermission


def rol_requerido(*codigos):
    class TieneRol(BasePermission):
        def has_permission(self, request, view):
            u = request.user
            return bool(u and u.is_authenticated and set(codigos) & u.codigos_roles)
    return TieneRol