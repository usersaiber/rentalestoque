# rental_system/urls.py
from django.urls import path
from equipment.admin import admin_site  # Certifique-se de que o caminho está correto e `admin_site` é importado de `equipment.admin`

urlpatterns = [
    path('admin/', admin_site.urls),  # Use o `admin_site` customizado aqui
    # outros URLs, se houver...
]
