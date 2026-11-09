"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.db import connection
from django.http import JsonResponse
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import LoginVista, me


def salud(request):
    try:
        connection.ensure_connection()
        return JsonResponse({"estado": "ok", "base_de_datos": connection.vendor})
    except Exception:
        return JsonResponse({"estado": "error"}, status=503)


urlpatterns = [
    path("api/health/", salud),
    path("api/auth/token/", LoginVista.as_view()),
    path("api/auth/refresh/", TokenRefreshView.as_view()),
    path("api/auth/me/", me),
    
    # Rutas de las aplicaciones del sistema modular
    path("api/", include("apps.personal.urls")),
    path("api/", include("apps.operations.urls")),
    path("api/synchronization/", include("apps.synchronization.urls")),
]