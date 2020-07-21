from django.test import TestCase

# Create your tests here.

class TesteVagaModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        print("Roda uma vez para criar o que vai ser usado nos testes. Aqui é colocado"+
        "o que não vai ser modificado nos testes")

    def setUp(self):
        print("Roda para modificar algo no que vai ser testado")
