
from django.contrib import admin
from django.urls import path
# core/urls.py
from django.contrib import admin
from django.urls import path, include  # Usa include para agregar las URLs de 'core'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # Incluye las URLs de la aplicación 'core'
]
