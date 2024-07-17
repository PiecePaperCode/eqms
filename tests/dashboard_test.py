import unittest

from django.test import Client, TestCase
from django.urls import reverse

from web.view import eqms


class TestDashboard(TestCase):
    def setUp(self):
        self.client = Client()

    def test_rendering_the_dashboard(self):
        url = reverse('dashboard')
        response = self.client.get(url)
        self.assertContains(response, 'Dunder Mifflin')

    def test_rendering_the_sidemenu(self):
        url = reverse('dashboard')
        response = self.client.get(url)
        self.assertContains(response, '01 Manual - Quality Manual')


if __name__ == '__main__':
    unittest.main()
