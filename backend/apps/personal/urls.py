from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PersonalViewSet, HojaDeVidaViewSet

router = DefaultRouter()
router.register(r'personal', PersonalViewSet)
router.register(r'hojas-de-vida', HojaDeVidaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]