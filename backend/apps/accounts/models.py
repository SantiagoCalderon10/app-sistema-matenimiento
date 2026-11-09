from django.db import models

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.functional import cached_property


class Rol(models.Model):
    codigo = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=80)

    class Meta:
        db_table = "roles"


class UsuarioManager(BaseUserManager):
    def create_user(self, nombre_usuario, password, personal, **extra):
        usuario = self.model(nombre_usuario=nombre_usuario, personal=personal, **extra)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario


class Usuario(AbstractBaseUser):
    personal = models.OneToOneField("personal.Personal", on_delete=models.PROTECT, related_name="usuario")
    nombre_usuario = models.CharField(max_length=60, unique=True)
    password = models.CharField(max_length=128, db_column="password_hash")
    activo = models.BooleanField(default=True)
    last_login = models.DateTimeField(db_column="ultimo_acceso", null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    roles = models.ManyToManyField(Rol, db_table="usuarios_roles", related_name="usuarios")

    USERNAME_FIELD = "nombre_usuario"
    objects = UsuarioManager()

    class Meta:
        db_table = "usuarios"

    @property
    def is_active(self):
        return self.activo

    @cached_property
    def codigos_roles(self):
        return frozenset(self.roles.values_list("codigo", flat=True))