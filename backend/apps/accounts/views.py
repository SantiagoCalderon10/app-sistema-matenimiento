from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class TokenConRoles(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, usuario):
        token = super().get_token(usuario)
        token["roles"] = sorted(usuario.codigos_roles)
        token["personal_id"] = usuario.personal_id
        return token


class LoginVista(TokenObtainPairView):
    serializer_class = TokenConRoles


@api_view(["GET"])
def me(request):
    u = request.user
    p = u.personal
    return Response({
        "id": u.id,
        "nombre_usuario": u.nombre_usuario,
        "roles": sorted(u.codigos_roles),
        "personal": {"id": p.id, "nombres": p.nombres, "apellidos": p.apellidos, "cargo": p.cargo},
    })