from django.test import TestCase
from rest_framework.test import APIClient

from .models import Product


class ProductAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.product = Product.objects.create(
            name='Test Mouse',
            description='A test mouse',
            price=500.00,
            stock=10
        )

    def test_product_list(self):
        response = self.client.get('/api/products/')

        self.assertEqual(response.status_code, 200)

    def test_product_search(self):
        response = self.client.get('/api/products/?search=Mouse')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'][0]['name'], 'Test Mouse')

    def test_purchase_reduces_stock(self):
        response = self.client.post(
            f'/api/products/{self.product.id}/purchase/',
            {'quantity': 3},
            format='json'
        )

        self.assertEqual(response.status_code, 200)

        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 7)

    def test_purchase_insufficient_stock(self):
        response = self.client.post(
            f'/api/products/{self.product.id}/purchase/',
            {'quantity': 100},
            format='json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data['error'],
            'Insufficient stock.'
        )