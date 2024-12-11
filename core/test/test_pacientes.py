from django.test import TestCase
from django.urls import reverse
from core.models import Paciente

class ListarPacientesTestCase(TestCase):
    def setUp(self):
        # Crear pacientes de prueba
        self.paciente1 = Paciente.objects.create(nombre="Paciente Uno", edad=30)
        self.paciente2 = Paciente.objects.create(nombre="Paciente Dos", edad=40)

    def test_listar_pacientes(self):
        response = self.client.get(reverse('listar_pacientes'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Paciente Uno")
        self.assertContains(response, "Paciente Dos")
