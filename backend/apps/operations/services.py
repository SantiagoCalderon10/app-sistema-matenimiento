from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Ejecucion, Evidencia, Revision

class OperationsService:

    @staticmethod
    @transaction.atomic
    def enviar_a_revision(ejecucion_id):
        """
        Valida que la ejecución posea evidencias de las tres etapas 
        (ANTES, DURANTE, DESPUES) antes de cambiar su estado a 'EN_REVISION'.
        """
        ejecucion = Ejecucion.objects.prefetch_related('evidencias').get(pk=ejecucion_id)
        
        etapas_presentes = set(ejecucion.evidencias.values_list('etapa', flat=True))
        etapas_requeridas = {'ANTES', 'DURANTE', 'DESPUES'}

        if not etapas_requeridas.issubset(etapas_presentes):
            raise ValidationError("La ejecución requiere obligatoriamente fotografías de las etapas: ANTES, DURANTE y DESPUES.")

        ejecucion.estado = 'EN_REVISION'
        ejecucion.save()
        return ejecucion

    @staticmethod
    @transaction.atomic
    def registrar_revision_supervisor(ejecucion_id, supervisor, aprobado, observaciones):
        """
        Registra la revisión del supervisor. Si es rechazado, deja abierta la puerta 
        para que se cree un nuevo intento de ejecución.
        """
        ejecucion = Ejecucion.objects.get(pk=ejecucion_id)
        
        Revision.objects.create(
            ejecucion=ejecucion,
            supervisor=supervisor,
            aprobado=aprobado,
            observaciones=observaciones
        )

        if aprobado:
            ejecucion.estado = 'APROBADO'
            ejecucion.asignacion.completada = True
            ejecucion.asignacion.save()
        else:
            ejecucion.estado = 'RECHAZADO'
            
            # Opcional: Auto-crear un nuevo intento para el operario tras el rechazo
            siguiente_intento = ejecucion.numero_intento + 1
            Ejecucion.objects.create(
                asignacion=ejecucion.asignacion,
                numero_intento=siguiente_intento,
                estado='PENDIENTE'
            )

        ejecucion.save()
        return ejecucion