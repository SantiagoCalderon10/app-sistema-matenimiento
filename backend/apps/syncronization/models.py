from django.conf import settings
from django.db import models

class Dispositivo(models.Model):
    operario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='dispositivos')
    dispositivo_uuid = models.CharField(max_length=255, unique=True)
    modelo = models.CharField(max_length=100, blank=True, null=True)
    registrado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dispositivo {self.modelo} - {self.operario.get_full_name()}"

class SincronizacionLog(models.Model):
    uuid_evento = models.UUIDField(unique=True) # UUID generado en el cliente por evento
    tipo_evento = models.CharField(max_length=100)
    procesado_exitosamente = models.BooleanField(default=True)
    recibido_en = models.DateTimeField(auto_now_add=True)
    respuesta_servidor = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"Evento {self.uuid_evento} ({self.tipo_evento})"