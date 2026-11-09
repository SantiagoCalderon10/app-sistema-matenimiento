from rest_framework import viewsets, permissions
from .models import Personal
from .serializers import PersonalSerializer
from .services import PersonalService
from rest_framework.response import Response
from rest_framework import status

class EsAdministradorOAdministrativo(permissions.BasePermission):
    """
    Permiso personalizado para restringir operaciones de escritura 
    solo a administradores y personal administrativo.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        # Suponiendo que el usuario tiene una relación con roles o banderas de tipo de usuario
        return request.user.is_staff or getattr(request.user, 'es_admin_o_administrativo', True)

class PersonalViewSet(viewsets.ModelViewSet):
    queryset = Personal.objects.all().select_related('user', 'hoja_de_vida')
    serializer_class = PersonalSerializer
    permission_classes = [permissions.IsAuthenticated, EsAdministradorOAdministrativo]

    def create(self, request, *args, **kwargs):
        """
        Sobrescribimos la creación para hacer uso de la capa de servicios 
        y mantener la lógica de negocio desacoplada de la vista.
        """
        user_data = request.data.get('user') # O ID de usuario existente
        datos_personal = {
            'documento_identidad': request.data.get('documento_identidad'),
            'telefono': request.data.get('telefono'),
            'cargo': request.data.get('cargo')
        }
        datos_hoja_vida = request.data.get('hoja_de_vida', {})

        # Nota: El usuario se debe asociar o crear previamente según la app 'accounts'
        # Aquí asumimos que recibimos una instancia de usuario o ID válido por simplicidad del ejemplo:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user_id = request.data.get('user_id')
        user = User.objects.get(pk=user_id)

        try:
            personal = PersonalService.crear_personal_con_hoja_de_vida(
                user=user, 
                datos_personal=datos_personal, 
                datos_hoja_vida=datos_hoja_vida
            )
            serializer = self.get_serializer(personal)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)