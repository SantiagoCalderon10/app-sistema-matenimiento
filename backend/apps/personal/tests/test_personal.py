import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.personal.models import Personal, HojaDeVida
from apps.personal.services import PersonalService

User = get_user_model()

@pytest.mark.django_db
class TestPersonalModule:

    @pytest.fixture
    def setup_user(self):
        # Crear un usuario administrativo de prueba
        admin_user = User.objects.create_user(
            username='admin_test',
            email='admin@empresa.com',
            password='password123',
            is_staff=True
        )
        # Crear un usuario base para asociar al operario
        operario_user = User.objects.create_user(
            username='operario_test',
            email='operario@empresa.com',
            password='password123'
        )
        return admin_user, operario_user

    def test_crear_personal_con_servicio(self, setup_user):
        admin_user, operario_user = setup_user
        
        datos_personal = {
            'documento_identidad': '123456789',
            'telefono': '3001234567',
            'cargo': 'Operario'
        }
        datos_hoja_vida = {
            'direccion': 'Calle Falsa 123',
            'contacto_emergencia_nombre': 'María Pérez',
            'contacto_emergencia_telefono': '3109876543',
            'completada': True
        }

        personal = PersonalService.crear_personal_con_hoja_de_vida(
            user=operario_user,
            datos_personal=datos_personal,
            datos_hoja_vida=datos_hoja_vida
        )

        assert personal.pk is not None
        assert personal.documento_identidad == '123456789'
        assert personal.hoja_de_vida.completada is True

    def test_validacion_documento_duplicado(self, setup_user):
        _, operario_user = setup_user
        
        # Primer registro
        Personal.objects.create(
            user=operario_user,
            documento_identidad='987654321',
            cargo='Operario'
        )

        # Intentar crear otro usuario con el mismo documento usando el servicio
        otro_user = User.objects.create_user(username='otro', email='otro@empresa.com', password='pwd')
        
        with pytest.raises(Exception):
            PersonalService.crear_personal_con_hoja_de_vida(
                user=otro_user,
                datos_personal={'documento_identidad': '987654321', 'cargo': 'Supervisor'},
                datos_hoja_vida={}
            )