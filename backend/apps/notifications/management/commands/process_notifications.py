from django.core.management.base import BaseCommand
from apps.notifications.services import NotificationService

class Command(BaseCommand):
    help = 'Procesa la cola persistente de notificaciones por correo'

    def handle(self, *args, **options):
        self.stdout.write("Iniciando procesamiento de notificaciones...")
        NotificationService.procesar_cola_pendiente()
        self.stdout.write(self.style.SUCCESS("Proceso de notificaciones finalizado."))
        