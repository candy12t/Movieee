from django.test import TestCase
from django.urls import reverse


class IndexViewsTest(TestCase):
  def test_index(self):
    response = self.client.get(reverse('movieee:index'))
    self.assertEqual(response.status_code, 200)