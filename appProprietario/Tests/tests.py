from django.test import TestCase

class AnimalTestCase(TestCase):
    
    def test_one_plus_one_equals_two(self):
        print("Method: test_one_plus_one_equals_two.")
        self.assertEqual(1 + 1, 2)

    def test_fazer_funcionar(self):
        self.assertEqual(2+2,4)
    
    def test_function_igual_a_dez(self):
        self.assertEqual(5 + 5,10)