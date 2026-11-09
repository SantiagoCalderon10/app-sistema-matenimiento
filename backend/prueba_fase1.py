from rest_framework.test import APIClient

c = APIClient()
print("health:", c.get("/api/health/").json())
r = c.post("/api/auth/token/", {"nombre_usuario": "admin", "password": "Admin2026!"}, format="json")
print("login:", r.status_code, list(r.json().keys()))
mal = c.post("/api/auth/token/", {"nombre_usuario": "admin", "password": "mala"}, format="json")
print("login con clave mala:", mal.status_code)
print("me sin token:", c.get("/api/auth/me/").status_code)
c.credentials(HTTP_AUTHORIZATION="Bearer " + r.json()["access"])
print("me con token:", c.get("/api/auth/me/").json())