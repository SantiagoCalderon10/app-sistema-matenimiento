from django.db import transaction
from .models import Personal, HojaDeVida
from django.core.exceptions import ValidationError

class PersonalService:
    @staticmethod
    @transaction.atomic
    def crear_personal_con_hoja_de_vida(user, datos_personal, datos_hoja_vida):
        """
        Crea el registro de personal y su respectiva hoja de vida de forma atómica.
        """
        if Personal.objects.filter(documento_identidad=datos_personal.get('documento_identidad')).exists():
            raise ValidationError("Ya existe un registro con este documento de identidad.")

        personal = Personal.objects.create(
            user=user,
            documento_identidad=datos_personal.get('documento_identidad'),
            telefono=datos_personal.get('telefono'),
            cargo=datos_personal.get('cargo')
        )

        HojaDeVida.objects.create(
            personal=personal,
            direccion=datos_hoja_vida.get('direccion', ''),
            contacto_emergencia_nombre=datos_hoja_vida.get('contacto_emergencia_nombre', ''),
            contacto_emergencia_telefono=datos_hoja_vida.get('contacto_emergencia_telefono', ''),
            estudios=datos_hoja_vida.get('estudios', ''),
            experiencia_previa=datos_hoja_vida.get('experiencia_previa', ''),
            completada=datos_hoja_vida.get('completada', False)
        )

        return personal