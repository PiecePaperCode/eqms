import unittest

from django.test import Client, TestCase
from django.urls import reverse


class TestDashboard(TestCase):
    def setUp(self):
        self.client = Client()

    def test_rendering_the_dashboard(self):
        url = reverse('dashboard')
        response = self.client.get(url)
        self.assertContains(response, 'Dunder Mifflin')

    def test_rendering_the_sidemenu(self):
        pass


if __name__ == '__main__':
    unittest.main()
