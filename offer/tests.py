import datetime

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import (APITestCase, APIRequestFactory,
                                 force_authenticate)

from offer.models import Offer
from offer.views import OfferViewSet
from stock_container.models import Inventory
from stock_management.models import Currency, Price, Stock

User = get_user_model()


class OfferViewSetTestCase(APITestCase):

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
        price = Price.objects.create(currency=cls.currency, value=500,
                                     date_of_change=datetime.datetime.now())
        cls.stock = Stock.objects.create(price=price)

        cls.offer = Offer.objects.create(stock=cls.stock, user=cls.user,
                                         entry_quantity=10, order_type='B',
                                         price=500, is_active=True)

        cls.offer2 = Offer.objects.create(stock=cls.stock, user=cls.admin,
                                          entry_quantity=10, order_type='B',
                                          price=500, is_active=True)

    def test_get_offer_list(self):
        offers_quantity = Offer.objects.all().count()
        url = reverse('offers-list')
        view = OfferViewSet.as_view({'get': 'list'})
        request = self.factory.get(url)
        force_authenticate(request, self.user, token=self.jwt_token)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), offers_quantity)

    def test_get_offer_list_by_not_auth_user(self):
        url = reverse('offers-list')
        view = OfferViewSet.as_view({'get': 'list'})
        request = self.factory.get(url)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_existing_offer(self):
        url = reverse('offers-detail', kwargs={"pk": self.offer.pk})
        view = OfferViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(url)
        force_authenticate(request, self.user, token=self.jwt_token)
        response = view(request, pk=self.offer.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.offer.id)

    def test_retrieve_existing_offer_not_auth_user(self):
        url = reverse('offers-detail', kwargs={"pk": self.offer.pk})
        view = OfferViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(url)
        response = view(request, pk=self.offer.pk)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_not_existing_offer(self):
        url = reverse('offers-detail', kwargs={"pk": 100})
        view = OfferViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(url)
        force_authenticate(request, self.user, token=self.jwt_token)
        response = view(request, pk=100)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_buy_offer(self):
        price2 = Price.objects.create(currency=self.currency, value=555,
                                      date_of_change=datetime.datetime.now())
        stock2 = Stock.objects.create(price=price2, name='Test',
                                      code='TST')

        offers_quantity_before = Offer.objects.all().count()
        url = reverse('offers-list')
        data = {'stock': stock2.id, 'entry_quantity': 5,
                'order_type': 'B', 'price': 5000}
        view = OfferViewSet.as_view({'post': 'create'})
        request = self.factory.post(url, data=data)
        force_authenticate(request, self.user, token=self.jwt_token)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(offers_quantity_before + 1,
                         Offer.objects.all().count())

    def test_create_sell_offer(self):
        Inventory.objects.create(user=self.user,
                                 stock=self.stock,
                                 quantity=10)
        offers_quantity_before = Offer.objects.all().count()
        url = reverse('offers-list')
        data = {'stock': self.stock.id, 'entry_quantity': 5,
                'order_type': 'S', 'price': 5000}
        view = OfferViewSet.as_view({'post': 'create'})
        request = self.factory.post(url, data=data)
        force_authenticate(request, self.user, token=self.jwt_token)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(offers_quantity_before + 1,
                         Offer.objects.all().count())

    def test_create_sell_offer_with_no_stocks_in_the_inventory(self):
        url = reverse('offers-list')
        data = {'stock': self.stock.id, 'entry_quantity': 5,
                'order_type': 'S', 'price': 5000}
        view = OfferViewSet.as_view({'post': 'create'})
        request = self.factory.post(url, data=data)
        force_authenticate(request, self.user, token=self.jwt_token)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_sell_offer_with_more_stocks_that_in_the_inventory(self):
        Inventory.objects.create(user=self.user, stock=self.stock,
                                 quantity=1)
        url = reverse('offers-list')
        data = {'stock': self.stock.id, 'entry_quantity': 10,
                'order_type': 'S', 'price': 5000}
        view = OfferViewSet.as_view({'post': 'create'})
        request = self.factory.post(url, data=data)
        force_authenticate(request, self.user, token=self.jwt_token)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_offer(self):
        url = reverse('offers-detail', kwargs={"pk": self.offer.pk})
        data = {'price': 50}
        view = OfferViewSet.as_view({'patch': 'partial_update'})
        request = self.factory.patch(url, data=data)
        force_authenticate(request, self.user, token=self.jwt_token)
        response = view(request, pk=self.offer.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Offer.objects.get(pk=self.offer.pk).price, 50)

    def test_update_not_user_offer(self):
        url = reverse('offers-detail', kwargs={"pk": self.offer2.pk})
        data = {'price': 50}
        view = OfferViewSet.as_view({'patch': 'partial_update'})
        request = self.factory.patch(url, data=data)
        force_authenticate(request, self.user, token=self.jwt_token)
        response = view(request, pk=self.offer2.pk)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_offer(self):
        objects_before = Offer.objects.all().count()
        url = reverse('offers-detail', kwargs={"pk": self.offer.pk})
        view = OfferViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete(url)
        force_authenticate(request, self.user, token=self.jwt_token)
        response = view(request, pk=self.offer.pk)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(objects_before - 1, Offer.objects.all().count())

    def test_delete_not_user_offer(self):
        objects_before = Offer.objects.all().count()
        url = reverse('offers-detail', kwargs={"pk": self.offer2.pk})
        view = OfferViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete(url)
        force_authenticate(request, self.user, token=self.jwt_token)
        response = view(request, pk=self.offer2.pk)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(objects_before, Offer.objects.all().count())
