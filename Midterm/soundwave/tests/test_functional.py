from django.test import TestCase
from django.urls import reverse
from api.models import Product

class OrderFunctionalTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(price=30.0)

    def test_order_page_loads(self):
        response = self.client.get(reverse('order-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order_form.html')

    def test_order_submission(self):
        response = self.client.post(reverse('order-create'), {'items': [{'product_id': self.product.id, 'quantity': 2}]})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('order-success'))
