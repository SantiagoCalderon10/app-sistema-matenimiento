from django.conf import settings
from django.db import models
from apps.personal.models import Personal

class CentroTrabajo(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    direccion = models.TextField()
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class TipoActividad(models.Model):
    nombre = models.CharField(max_length=100, unique=True) # Ej: Pintura, Jardinería, Piscinas
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Programacion(models.Model):
    semana_inicio = models.DateField()
    semana_fin = models.DateField()
    creada_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)
    publicada = models.BooleanField(default=False)
    creada_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Programación Semanal: {self.semana_inicio} al {self.semana_fin}"

class Asignacion(models.Model):
    programacion = models.ForeignKey(Programacion, on_delete=models.CASCADE, related_name='asignaciones')
    operario = models.ForeignKey(Personal, on_delete=models.RESTRICT, related_name='asignaciones')
    centro_trabajo = models.ForeignKey(CentroTrabajo, on_delete=models.RESTRICT, related_name='asignaciones')
    tipo_actividad = models.ForeignKey(TipoActividad, on_delete=models.RESTRICT)
    supervisor = models.ForeignKey(Personal, on_delete=models.RESTRICT, related_name='supervisiones', blank=True, null=True)
    fecha_programada = models.DateField()
    completada = models.BooleanField(default=False)

    def __str__(self):
        return f"Asignación: {self.tipo_actividad} en {self.centro_trabajo} -> {self.operario}"

class RegistroCentro(models.Model):
    asignacion = models.ForeignKey(Asignacion, on_delete=models.CASCADE, related_name='registros_centro')
    hora_entrada = models.DateTimeField(blank=True, null=True)
    hora_salida = models.DateTimeField(blank=True, null=True)

class Ejecucion(models.Model):
    asignacion = models.ForeignKey(Asignacion, on_delete=models.CASCADE, related_name='ejecuciones')
    numero_intento = models.PositiveIntegerField(default=1)
    hora_inicio = models.DateTimeField(blank=True, null=True)
    hora_fin = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(
        max_length=30,
        choices=[('PENDIENTE', 'Pendiente'), ('EN_PROCESO', 'En Proceso'), ('EN_REVISION', 'En Revisión'), ('APROBADO', 'Aprobado'), ('RECHAZADO', 'Rechazado')],
        default='PENDIENTE'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['asignacion', 'numero_intento'], name='unique_asignacion_intento')
        ]

    def __str__(self):
        return f"Ejecución #{self.numero_intento} - Asignación {self.asignacion_id}"

class Evidencia(models.Model):
    ETAPA_CHOICES = [('ANTES', 'Antes'), ('DURANTE', 'Durante'), ('DESPUES', 'Después')]
    ejecucion = models.ForeignKey(Ejecucion, on_delete=models.CASCADE, related_name='evidencias')
    etapa = models.CharField(max_length=20, choices=ETAPA_CHOICES)
    archivo_ruta = models.CharField(max_length=255) # Ruta del archivo o almacenamiento
    latitud = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    creada_en = models.DateTimeField(auto_now_add=True)

class Revision(models.Model):
    ejecucion = models.ForeignKey(Ejecucion, on_delete=models.CASCADE, related_name='revisiones')
    supervisor = models.ForeignKey(Personal, on_delete=models.RESTRICT)
    aprobado = models.BooleanField()
    observaciones = models.TextField(blank=True, null=True)
    revisada_en = models.DateTimeField(auto_now_add=True)