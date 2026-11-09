from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import CentroTrabajo, TipoActividad, Programacion, Asignacion, RegistroCentro, Ejecucion, Evidencia
from .serializers import (
    CentroTrabajoSerializer, TipoActividadSerializer, ProgramacionSerializer, 
    AsignacionSerializer, RegistroCentroSerializer, EjecucionSerializer, EvidenciaSerializer
)
from .services import OperationsService

class CentroTrabajoViewSet(viewsets.ModelViewSet):
    queryset = CentroTrabajo.objects.all()
    serializer_class = CentroTrabajoSerializer
    permission_classes = [permissions.IsAuthenticated]

class TipoActividadViewSet(viewsets.ModelViewSet):
    queryset = TipoActividad.objects.all()
    serializer_class = TipoActividadSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProgramacionViewSet(viewsets.ModelViewSet):
    queryset = Programacion.objects.all().prefetch_related('asignaciones__centro_trabajo', 'asignaciones__tipo_actividad')
    serializer_class = ProgramacionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creada_por=self.request.user)

class AsignacionViewSet(viewsets.ModelViewSet):
    queryset = Asignacion.objects.all().select_related('operario', 'centro_trabajo', 'tipo_actividad', 'supervisor')
    serializer_class = AsignacionSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def registrar_centro(self, request, pk=None):
        """Registra la hora de entrada o salida del centro de trabajo."""
        asignacion = self.get_object()
        tipo_marca = request.data.get('tipo') # 'entrada' o 'salida'
        
        registro, created = RegistroCentro.objects.get_or_create(asignacion=asignacion)
        ahora = timezone.now()

        if tipo_marca == 'entrada':
            registro.hora_entrada = ahora
        elif tipo_marca == 'salida':
            registro.hora_salida = ahora
        else:
            return Response({"error": "Tipo de marca inválido (use 'entrada' o 'salida')"}, status=status.HTTP_400_BAD_REQUEST)

        registro.save()
        return Response(RegistroCentroSerializer(registro).data, status=status.HTTP_200_OK)

class EjecucionViewSet(viewsets.ModelViewSet):
    queryset = Ejecucion.objects.all().prefetch_related('evidencias', 'revisiones')
    serializer_class = EjecucionSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def enviar_revision(self, request, pk=None):
        """Valida las 3 etapas fotográficas y envía a revisión."""
        try:
            ejecucion = OperationsService.enviar_a_revision(pk)
            return Response({"mensaje": "Ejecución enviada a revisión correctamente.", "estado": ejecucion.estado}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def revisar(self, request, pk=None):
        """Permite al supervisor aprobar o rechazar el trabajo."""
        aprobado = request.data.get('aprobado')
        observaciones = request.data.get('observaciones', '')
        
        # Suponiendo que el usuario autenticado tiene relación con el perfil Personal de supervisor
        try:
            supervisor_perfil = request.user.perfil_personal
        except Exception:
            return Response({"error": "El usuario actual no tiene un perfil de personal asociado."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ejecucion = OperationsService.registrar_revision_supervisor(
                ejecucion_id=pk,
                supervisor=supervisor_perfil,
                aprobado=aprobado,
                observaciones=observaciones
            )
            return Response({"mensaje": "Revisión registrada con éxito.", "estado": ejecucion.estado}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class EvidenciaViewSet(viewsets.ModelViewSet):
    queryset = Evidencia.objects.all()
    serializer_class = EvidenciaSerializer
    permission_classes = [permissions.IsAuthenticated]