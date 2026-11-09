from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CentroTrabajoViewSet, TipoActividadViewSet, ProgramacionViewSet, AsignacionViewSet, EjecucionViewSet, EvidenciaViewSet

router = DefaultRouter()
router.register(r'centros', CentroTrabajoViewSet)
router.register(r'actividades', TipoActividadViewSet)
router.register(r'programaciones', ProgramacionViewSet)
router.register(r'asignaciones', AsignacionViewSet)
router.register(r'ejecuciones', EjecucionViewSet)
router.register(r'evidencias', EvidenciaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]