from rest_framework import serializers
from .models import Personal, HojaDeVida

class HojaDeVidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = HojaDeVida
        fields = [
            'id', 'direccion', 'contacto_emergencia_nombre', 
            'contacto_emergencia_telefono', 'estudios', 
            'experiencia_previa', 'completada', 'actualizada_en'
        ]

class PersonalSerializer(serializers.ModelSerializer):
    hoja_de_vida = HojaDeVidaSerializer(required=False)
    nombre_completo = serializers.CharField(source='user.get_full_name', read_only=True)
    correo = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Personal
        fields = [
            'id', 'user', 'nombre_completo', 'correo', 
            'documento_identidad', 'telefono', 'cargo', 
            'activo', 'hoja_de_vida', 'creado_en', 'actualizado_en'
        ]
        read_only_fields = ['creado_en', 'actualizado_en']

    def validate_documento_identidad(self, value):
        # Validación para evitar duplicados en actualizaciones o creaciones
        instance = getattr(self, 'instance', None)
        if Personal.objects.filter(documento_identidad=value).exclude(pk=instance.pk if instance else None).exists():
            raise serializers.ValidationError("Ya existe un registro con este documento de identidad.")
        return value