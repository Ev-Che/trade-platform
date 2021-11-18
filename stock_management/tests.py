import datetime

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import (APITestCase, APIRequestFactory,
                                 force_authenticate)

from stock_management.models import Stock, Currency, Price
from stock_management.views import StockViewSet

User = get_user_model()


class StockViewSetTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.factory = APIRequestFactory()
        jwt_url = reverse('jwt-create')
        cls.user = User.objects.create(username='test', password='test')
        cls.jwt_token = cls.factory.get(jwt_url)
        currency = Currency.objects.create(code='USD', name='US Dollar')
        price = Price.objects.create(currency=currency, value=500,
                                     date_of_change=datetime.datetime.now())
        cls.stock = Stock.objects.create(price=price)

    def test_get_stock_list(self):
        url = reverse('stocks-list')
        objects_before = Stock.objects.all().count()
        view = StockViewSet.as_view({'get': 'list'})
        request = self.factory.get(url)
        force_authenticate(request, self.user, token=self.jwt_token)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(objects_before, len(response.data))

    def test_retrieve_existing_stock(self):
        url = reverse('stocks-detail', kwargs={"pk": self.stock.pk})
        view = StockViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(url)
        force_authenticate(request, self.user, token=self.jwt_token)
        response = view(request, pk=self.stock.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), self.stock.id)

    def test_retrieve_non_existing_stock(self):
        url = reverse('stocks-detail', kwargs={"pk": 5})
        view = StockViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(url)
        force_authenticate(request, self.user, token=self.jwt_token)
        response = view(request, pk=5)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
