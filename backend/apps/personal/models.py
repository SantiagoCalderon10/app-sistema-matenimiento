from django.db import models


class Personal(models.Model):
    class Cargo(models.TextChoices):
        ADMIN = "ADMIN"
        ADMINISTRATIVO = "ADMINISTRATIVO"
        SUPERVISOR = "SUPERVISOR"
        OPERARIO = "OPERARIO"

    class Estado(models.TextChoices):
        ACTIVO = "ACTIVO"
        INACTIVO = "INACTIVO"

    tipo_documento = models.CharField(max_length=2)
    numero_documento = models.CharField(max_length=30, unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    telefono = models.CharField(max_length=30, blank=True)
    correo_institucional = models.EmailField(unique=True)
    cargo = models.CharField(max_length=20, choices=Cargo.choices)
    fecha_ingreso = models.DateField()
    estado = models.CharField(max_length=10, choices=Estado.choices, default=Estado.ACTIVO)

    class Meta:
        db_table = "personal"


class HojaVida(models.Model):
    personal = models.OneToOneField(Personal, on_delete=models.CASCADE, related_name="hoja_vida")
    perfil_profesional = models.TextField(blank=True)
    nivel_educativo = models.CharField(max_length=80, blank=True)
    experiencia_laboral = models.TextField(blank=True)
    formacion_adicional = models.TextField(blank=True)
    documento_url = models.CharField(max_length=255, blank=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "hojas_vida"