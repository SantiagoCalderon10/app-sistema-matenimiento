from rest_framework import views, permissions, status
from rest_framework.response import Response
from .models import SincronizacionLog
from apps.operations.models import RegistroCentro, Ejecucion, Evidencia
from django.utils import timezone
from datetime import timedelta

class SyncAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        uuid_evento = data.get('uuid')
        tipo_evento = data.get('tipo')
        datos_evento = data.get('datos', {})
        timestamp_local_str = data.get('timestamp_local')

        if not uuid_evento or not tipo_evento:
            return Response({"error": "Faltan parámetros obligatorios (uuid o tipo)"}, status=status.HTTP_400_BAD_REQUEST)

        # 1. Verificar idempotencia: Si el UUID ya fue procesado, retornar éxito de inmediato
        if SincronizacionLog.objects.filter(uuid_evento=uuid_evento).exists():
            return Response({"mensaje": "Evento ya sincronizado previamente (idempotente).", "uuid": uuid_evento}, status=status.HTTP_200_OK)

        # 2. Control de desfase de reloj (Regla del informe: marcar si supera los 5 minutos)
        desfase_advertencia = False
        if timestamp_local_str:
            try:
                from django.utils.dateparse import parse_datetime
                ts_local = parse_datetime(timestamp_local_str)
                if ts_local:
                    ahora = timezone.now()
                    if abs(ahora - ts_local) > timedelta(minutes=5):
                        desfase_advertencia = True
            except Exception:
                pass

        try:
            # 3. Procesar según el tipo de evento recibido offline
            if tipo_evento == 'REGISTRO_CENTRO':
                asignacion_id = datos_evento.get('asignacion_id')
                tipo_marca = datos_evento.get('tipo_marca') # 'entrada' o 'salida'
                registro, _ = RegistroCentro.objects.get_or_create(asignacion_id=asignacion_id)
                
                if tipo_marca == 'entrada':
                    registro.hora_entrada = datos_evento.get('hora', timezone.now())
                elif tipo_marca == 'salida':
                    registro.hora_salida = datos_evento.get('hora', timezone.now())
                registro.save()

            elif tipo_evento == 'EVIDENCIA_FOTO':
                ejecucion_id = datos_evento.get('ejecucion_id')
                Evidencia.objects.create(
                    ejecucion_id=ejecucion_id,
                    etapa=datos_evento.get('etapa'), # ANTES, DURANTE, DESPUES
                    archivo_ruta=datos_evento.get('archivo_ruta'),
                    latitud=datos_evento.get('latitud'),
                    longitud=datos_evento.get('longitud')
                )

            # 4. Registrar en el log de sincronización para asegurar idempotencia futura
            SincronizacionLog.objects.create(
                uuid_evento=uuid_evento,
                tipo_evento=tipo_evento,
                procesado_exitosamente=True,
                respuesta_servidor={"desfase_reloj": desfase_advertencia}
            )

            return Response({
                "mensaje": "Sincronización procesada con éxito",
                "uuid": uuid_evento,
                "advertencia_desfase": desfase_advertencia
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)