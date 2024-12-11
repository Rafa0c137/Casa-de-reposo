from django.test import TestCase
from core.views import generar_qr_code
from django.conf import settings
import os
from PIL import Image
import qrcode

class QRCodeGenerationTests(TestCase):
    def setUp(self):
        # Configuración inicial antes de cada prueba
        self.paciente_id = 1
        self.data = "Paciente: Juan Pérez\nEdad: 30\nID: 1"
        self.qr_code_directory = os.path.join(settings.MEDIA_ROOT, 'qr_codes')

    def test_qr_code_generation(self):
        # Generar el QR
        qr_code_path = generar_qr_code(self.data, self.paciente_id)

        # Verificar que el archivo QR se generó
        self.assertTrue(os.path.exists(qr_code_path), "El archivo QR no fue creado.")

        # Verificar que el archivo es una imagen válida
        with Image.open(qr_code_path) as img:
            self.assertEqual(img.format, 'PNG', "El archivo generado no es una imagen PNG válida.")

    def tearDown(self):
        # Limpieza después de cada prueba
        qr_code_path = os.path.join(self.qr_code_directory, f"{self.paciente_id}.png")
        if os.path.exists(qr_code_path):
            os.remove(qr_code_path)
