from .models import Notificacion
from .adapters import SMTPEmailAdapter
from django.utils import timezone

class NotificationService:
    @staticmethod
    def encolar_notificacion(usuario, asunto, mensaje):
        return Notificacion.objects.create(
            destinatario=usuario,
            asunto=asunto,
            mensaje=mensaje
        )

    @staticmethod
    def procesar_cola_pendiente():
        """Procesa las notificaciones en estado PENDIENTE con control de reintentos."""
        pendientes = Notificacion.objects.filter(estado='PENDIENTE', intentos__lt=3)
        
        for notif in pendientes:
            notif.intentos += 1
            try:
                SMTPEmailAdapter.enviar_correo(
                    destinatario_email=notif.destinatario.email,
                    asunto=notif.asunto,
                    mensaje=notif.mensaje
                )
                notif.estado = 'ENVIADO'
                notif.enviada_en = timezone.now()
                notif.error_log = None
            except Exception as e:
                notif.estado = 'FALLIDO' if notif.intentos >= 3 else 'PENDIENTE'
                notif.error_log = str(e)
            notif.save()