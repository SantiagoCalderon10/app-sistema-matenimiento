from apps.accounts.models import Rol, Usuario
from apps.personal.models import Personal

for codigo, nombre in [("ADMIN", "Administrador"), ("ADMINISTRATIVO", "Administrativo"),
                       ("SUPERVISOR", "Supervisor"), ("OPERARIO", "Operario")]:
    Rol.objects.get_or_create(codigo=codigo, defaults={"nombre": nombre})

if not Usuario.objects.filter(nombre_usuario="admin").exists():
    p = Personal.objects.create(tipo_documento="CC", numero_documento="1000", nombres="Admin",
                                apellidos="Sistema", correo_institucional="admin@empresa.local",
                                cargo="ADMIN", fecha_ingreso="2026-01-01")
    u = Usuario.objects.create_user("admin", "Admin2026!", p)
    u.roles.add(Rol.objects.get(codigo="ADMIN"))
print("Listo: roles y usuario admin creados")