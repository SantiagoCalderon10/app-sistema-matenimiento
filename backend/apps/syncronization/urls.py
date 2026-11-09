from django.urls import path
from .views import SyncAPIView

urlpatterns = [
    path('sync/', SyncAPIView.as_view(), name='api-sincronizacion'),
]