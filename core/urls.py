# core/urls.py
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView  # Importa las vistas genéricas de autenticación
from .views import registrar_paciente, listar_pacientes, detalle_paciente
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('registrar/', registrar_paciente, name='registrar_paciente'),
    path('pacientes/', listar_pacientes, name='listar_pacientes'),
    path('paciente/<int:paciente_id>/', detalle_paciente, name='detalle_paciente'), 
    path('registro_usuario/', views.registrar_usuario, name='registro_usuario'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),  # Usa LoginView
    path('logout/', LogoutView.as_view(), name='logout'),  # Usa LogoutView,
    path('paciente/<int:paciente_id>/descargar_qr/', views.descargar_qr, name='descargar_qr'),
    

    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)