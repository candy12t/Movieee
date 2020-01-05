from django.test import TestCase, Client
from django.urls import reverse


class IndexViewsTest(TestCase):
  def test_index(self):
    response = Client().get(reverse('movieee:index'))
    self.assertEqual(response.status_code, 200)