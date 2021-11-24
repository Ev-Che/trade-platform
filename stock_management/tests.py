import datetime

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import (APITestCase, APIRequestFactory,
                                 force_authenticate)

from stock_management.models import Stock, Currency, Price
from stock_management.views import StockViewSet, CurrencyViewSet, PriceViewSet

User = get_user_model()


class StockViewSetTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.factory = APIRequestFactory()
        jwt_url = reverse('jwt-create')
        cls.user = User.objects.create_user(username='test', password='test')
        cls.admin = User.objects.create_superuser(username='admin',
                                                  password='admin')
        cls.jwt_token = cls.factory.get(jwt_url)
        currency = Currency.objects.create(code='USD', name='US Dollar')
        price = Price.objects.create(currency=currency, value=500,
                                     date_of_change=datetime.datetime.now())
        cls.stock = Stock.objects.create(price=price)

    def test_get_stock_list(self):
        url = reverse('stocks-list')
        view = StockViewSet.as_view({'get': 'list'})
        request = self.factory.get(url)
        force_authenticate(request, self.user, token=self.jwt_token)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_existing_stock(self):
        url = reverse('stocks-detail', kwargs={"pk": self.stock.pk})
        view = StockViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(url)
        force_authenticate(request, self.user, token=self.jwt_token)
        response = view(request, pk=self.stock.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_not_auth_user(self):
        url = reverse('stocks-list')
        view = StockViewSet.as_view({'get': 'list'})
        request = self.factory.get(url)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_not_auth_user(self):
        url = reverse('stocks-detail', kwargs={"pk": self.stock.pk})
        view = StockViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(url)
        response = view(request, pk=self.stock.pk)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_non_existing_stock(self):
        url = reverse('stocks-detail', kwargs={"pk": 5})
        view = StockViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(url)
        force_authenticate(request, self.user, token=self.jwt_token)
        response = view(request, pk=5)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_try_to_edit_stock_not_admin(self):
        url = reverse('stocks-detail', {"pk": 1})
        view = StockViewSet.as_view({'patch': 'partial_update'})
        request = self.factory.patch(url, data={"details": "test edit"})
        force_authenticate(request, self.user, token=self.jwt_token)
        response = view(request, pk=1)

        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)

    def test_try_to_delete_stock_not_admin(self):
        url = reverse('stocks-detail', {"pk": 1})
        view = StockViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete(url)
        force_authenticate(request, self.user, token=self.jwt_token)
        response = view(request, pk=1)

        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)

    def test_edit_stock_by_admin(self):
        url = reverse('stocks-detail', {"pk": 1})
        view = StockViewSet.as_view({'patch': 'partial_update'})
        request = self.factory.patch(url, data={"details": "test edit"})
        force_authenticate(request, self.admin, token=self.jwt_token)
        response = view(request, pk=1)

        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

    def test_delete_stock_by_admin(self):
        url = reverse('stocks-detail', {"pk": 1})
        view = StockViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete(url)
        force_authenticate(request, self.admin, token=self.jwt_token)
        response = view(request, pk=1)

        self.assertEqual(response.status_code,
                         status.HTTP_204_NO_CONTENT)


class CurrencyViewSetTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.factory = APIRequestFactory()
        jwt_url = reverse('jwt-create')
        cls.user = User.objects.create_user(username='test', password='test')
        cls.admin = User.objects.create_superuser(username='admin',
                                                  password='admin')
        cls.jwt_token = cls.factory.get(jwt_url)
        cls.currency = Currency.objects.create(code='USD', name='US Dollar')

    def test_get_currencies_list(self):
        url = reverse('currencies-list')
        view = CurrencyViewSet.as_view({'get': 'list'})
        request = self.factory.get(url)
        force_authenticate(request, self.user, token=self.jwt_token)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_existing_currency(self):
        url = reverse('currencies-detail', kwargs={"pk": self.currency.pk})
        view = CurrencyViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(url)
        force_authenticate(request, self.user, token=self.jwt_token)
        response = view(request, pk=self.currency.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_not_auth_user(self):
        url = reverse('currencies-list')
        view = CurrencyViewSet.as_view({'get': 'list'})
        request = self.factory.get(url)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_not_auth_user(self):
        url = reverse('currencies-detail', kwargs={"pk": self.currency.pk})
        view = CurrencyViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(url)
        response = view(request, pk=self.currency.pk)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_non_existing_currency(self):
        url = reverse('currencies-detail', kwargs={"pk": 5})
        view = CurrencyViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(url)
        force_authenticate(request, self.user, token=self.jwt_token)
        response = view(request, pk=5)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_try_to_edit_currency_not_admin(self):
        url = reverse('currencies-detail', {"pk": 1})
        view = CurrencyViewSet.as_view({'patch': 'partial_update'})
        request = self.factory.patch(url, data={"name": "test name"})
        force_authenticate(request, self.user, token=self.jwt_token)
        response = view(request, pk=1)

        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)

    def test_try_to_delete_currency_not_admin(self):
        url = reverse('currencies-detail', {"pk": 1})
        view = CurrencyViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete(url)
        force_authenticate(request, self.user, token=self.jwt_token)
        response = view(request, pk=1)

        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)

    def test_edit_currency_by_admin(self):
        url = reverse('currencies-detail', {"pk": 1})
        view = CurrencyViewSet.as_view({'patch': 'partial_update'})
        request = self.factory.patch(url, data={"name": "test name"})
        force_authenticate(request, self.admin, token=self.jwt_token)
        response = view(request, pk=1)

        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

    def test_delete_currency_by_admin(self):
        url = reverse('currencies-detail', {"pk": 1})
        view = CurrencyViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete(url)
        force_authenticate(request, self.admin, token=self.jwt_token)
        response = view(request, pk=1)

        self.assertEqual(response.status_code,
                         status.HTTP_204_NO_CONTENT)


class PriceViewSetTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.factory = APIRequestFactory()
        jwt_url = reverse('jwt-create')
        cls.user = User.objects.create_user(username='test', password='test')
        cls.admin = User.objects.create_superuser(username='admin',
                                                  password='admin')
        cls.jwt_token = cls.factory.get(jwt_url)
        currency = Currency.objects.create(code='USD', name='US Dollar')
        cls.price = Price.objects.create(
            currency=currency, value=500,
            date_of_change=datetime.datetime.now())

    def test_get_prices_list(self):
        url = reverse('prices-list')
        view = PriceViewSet.as_view({'get': 'list'})
        request = self.factory.get(url)
        force_authenticate(request, self.user, token=self.jwt_token)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_existing_price(self):
        url = reverse('prices-detail', kwargs={"pk": self.price.pk})
        view = PriceViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(url)
        force_authenticate(request, self.user, token=self.jwt_token)
        response = view(request, pk=self.price.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_not_auth_user(self):
        url = reverse('currencies-list')
        view = CurrencyViewSet.as_view({'get': 'list'})
        request = self.factory.get(url)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_not_auth_user(self):
        url = reverse('prices-detail', kwargs={"pk": self.price.pk})
        view = PriceViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(url)
        response = view(request, pk=self.price.pk)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_non_existing_price(self):
        url = reverse('prices-detail', kwargs={"pk": 5})
        view = PriceViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(url)
        force_authenticate(request, self.user, token=self.jwt_token)
        response = view(request, pk=5)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_try_to_edit_price_not_admin(self):
        url = reverse('prices-detail', {"pk": 1})
        view = PriceViewSet.as_view({'patch': 'partial_update'})
        request = self.factory.patch(url, data={"value": 0.0})
        force_authenticate(request, self.user, token=self.jwt_token)
        response = view(request, pk=1)

        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)

    def test_try_to_delete_price_not_admin(self):
        url = reverse('prices-detail', {"pk": 1})
        view = PriceViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete(url)
        force_authenticate(request, self.user, token=self.jwt_token)
        response = view(request, pk=1)

        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)

    def test_edit_price_by_admin(self):
        url = reverse('prices-detail', {"pk": 1})
        view = PriceViewSet.as_view({'patch': 'partial_update'})
        request = self.factory.patch(url, data={"value": 0.0})
        force_authenticate(request, self.admin, token=self.jwt_token)
        response = view(request, pk=1)

        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

    def test_delete_price_by_admin(self):
        url = reverse('prices-detail', {"pk": 1})
        view = PriceViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete(url)
        force_authenticate(request, self.admin, token=self.jwt_token)
        response = view(request, pk=1)

        self.assertEqual(response.status_code,
                         status.HTTP_204_NO_CONTENT)
