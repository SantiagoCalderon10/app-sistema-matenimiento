from django.conf import settings
from django.db import models

class Notificacion(models.Model):
    destinatario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notificaciones')
    asunto = models.CharField(max_length=255)
    mensaje = models.TextField()
    estado = models.CharField(
        max_length=20,
        choices=[('PENDIENTE', 'Pendiente'), ('ENVIADO', 'Enviado'), ('FALLIDO', 'Fallido')],
        default='PENDIENTE'
    )
    intentos = models.PositiveIntegerField(default=0)
    creada_en = models.DateTimeField(auto_now_add=True)
    enviada_en = models.DateTimeField(blank=True, null=True)
    error_log = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Notificación para {self.destinatario.email} - {self.estado}"