from rest_framework import serializers
from .models import CentroTrabajo, TipoActividad, Programacion, Asignacion, RegistroCentro, Ejecucion, Evidencia, Revision

class CentroTrabajoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CentroTrabajo
        fields = '__all__'

class TipoActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoActividad
        fields = '__all__'

class EvidenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evidencia
        fields = ['id', 'ejecucion', 'etapa', 'archivo_ruta', 'latitud', 'longitud', 'creada_en']
        read_only_fields = ['creada_en']

class RevisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revision
        fields = ['id', 'ejecucion', 'supervisor', 'aprobado', 'observaciones', 'revisada_en']
        read_only_fields = ['revisada_en']

class EjecucionSerializer(serializers.ModelSerializer):
    evidencias = EvidenciaSerializer(many=True, read_only=True)
    revisiones = RevisionSerializer(many=True, read_only=True)

    class Meta:
        model = Ejecucion
        fields = ['id', 'asignacion', 'numero_intento', 'hora_inicio', 'hora_fin', 'estado', 'evidencias', 'revisiones']

class RegistroCentroSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroCentro
        fields = ['id', 'asignacion', 'hora_entrada', 'hora_salida']

class AsignacionSerializer(serializers.ModelSerializer):
    centro_trabajo_nombre = serializers.CharField(source='centro_trabajo.nombre', read_only=True)
    tipo_actividad_nombre = serializers.CharField(source='tipo_actividad.nombre', read_only=True)
    operario_nombre = serializers.CharField(source='operario.user.get_full_name', read_only=True)
    registros_centro = RegistroCentroSerializer(many=True, read_only=True)
    ejecuciones = EjecucionSerializer(many=True, read_only=True)

    class Meta:
        model = Asignacion
        fields = [
            'id', 'programacion', 'operario', 'operario_nombre', 
            'centro_trabajo', 'centro_trabajo_nombre', 'tipo_actividad', 
            'tipo_actividad_nombre', 'supervisor', 'fecha_programada', 
            'completada', 'registros_centro', 'ejecuciones'
        ]

class ProgramacionSerializer(serializers.ModelSerializer):
    asignaciones = AsignacionSerializer(many=True, read_only=True)

    class Meta:
        model = Programacion
        fields = ['id', 'semana_inicio', 'semana_fin', 'creada_por', 'publicada', 'creada_en', 'asignaciones']
        read_only_fields = ['creada_en', 'creada_por']