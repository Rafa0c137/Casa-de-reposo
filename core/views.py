from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
import os
import qrcode

from .models import Paciente
from .forms import PacienteForm
from django.contrib.auth.forms import UserCreationForm


# Función para generar códigos QR y guardarlos en un archivo
def generar_qr_code(data, paciente_id):
    # Directorio para guardar los códigos QR
    qr_code_directory = os.path.join(settings.MEDIA_ROOT, 'qr_codes')
    os.makedirs(qr_code_directory, exist_ok=True)

    # Generar el código QR
    qr = qrcode.make(data)
    file_path = os.path.join(qr_code_directory, f"{paciente_id}.png")
    qr.save(file_path)  # Guarda el archivo en el directorio

    return file_path  # Devuelve la ruta del archivo


# Vista principal
def home(request):
    return render(request, 'home.html')


# Vista para listar pacientes
def listar_pacientes(request):
    pacientes = Paciente.objects.all()  # Obtén todos los pacientes
    return render(request, 'listar_pacientes.html', {'pacientes': pacientes})


# Vista para registrar un usuario
@user_passes_test(lambda u: u.is_superuser)
def registrar_usuario(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_pacientes')
    else:
        form = UserCreationForm()
    return render(request, 'registro_usuario.html', {'form': form})


# Vista para registrar un paciente
@user_passes_test(lambda user: user.is_staff)  # Solo para usuarios administradores
def registrar_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el nuevo paciente en la base de datos
            return redirect('listar_pacientes')  # Redirige a la lista de pacientes después de registrar
    else:
        form = PacienteForm()

    return render(request, 'registrar_paciente.html', {'form': form})


# Vista para mostrar detalles de un paciente
def detalle_paciente(request, paciente_id):
    # Obtén el paciente o lanza un error 404 si no existe
    paciente = get_object_or_404(Paciente, id=paciente_id)

    # Genera los datos del QR
    data = f"Nombre: {paciente.nombre}, ID: {paciente.id}"

    # Genera y guarda el código QR
    generar_qr_code(data, paciente.id)

    # Calcula la URL del archivo QR para la plantilla
    qr_code_url = os.path.join(settings.MEDIA_URL, 'qr_codes', f"{paciente.id}.png")

    return render(request, 'detalle_paciente.html', {
        'paciente': paciente,
        'qr_code_path': qr_code_url,  # URL del QR para la plantilla
    })


# Vista para descargar el código QR de un paciente
def descargar_qr(request, paciente_id):
    # Obtén el paciente o lanza un error 404 si no existe
    paciente = get_object_or_404(Paciente, id=paciente_id)

    # Construye la ruta del archivo QR
    qr_code_path = os.path.join(settings.MEDIA_ROOT, 'qr_codes', f"{paciente.id}.png")

    # Verifica si el archivo existe
    if not os.path.exists(qr_code_path):
        return HttpResponse("El archivo QR no se encontró.", status=404)

    # Prepara la respuesta para descargar el archivo
    with open(qr_code_path, 'rb') as qr_file:
        response = HttpResponse(qr_file.read(), content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename="{paciente.id}.png"'
        return response
