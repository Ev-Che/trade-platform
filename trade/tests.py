import datetime

from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import (APITestCase, APIRequestFactory,
                                 force_authenticate)

from offer.models import Offer
from stock_management.models import Currency, Price, Stock
from trade.models import Trade
from trade.views import TradeViewSet

User = get_user_model()


class TradeViewSetTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.factory = APIRequestFactory()
        jwt_url = reverse('jwt-create')
        cls.user = User.objects.create_user(username='test', password='test')
        cls.admin = User.objects.create_superuser(username='admin',
                                                  password='admin')
        cls.user2 = User.objects.create_user(username='test2',
                                             password='test2')
        cls.jwt_token = cls.factory.get(jwt_url)
        cls.currency = Currency.objects.create(code='USD', name='US Dollar')
        price = Price.objects.create(currency=cls.currency, value=500,
                                     date_of_change=datetime.datetime.now())
        stock = Stock.objects.create(price=price)

        user_buy_offer = Offer.objects.create(stock=stock, user=cls.user,
                                              entry_quantity=10,
                                              order_type='B',
                                              price=500, is_active=True)

        admin_sell_offer = Offer.objects.create(stock=stock,
                                                user=cls.admin,
                                                entry_quantity=10,
                                                order_type='S',
                                                price=500, is_active=True)
        user2_buy_offer = Offer.objects.create(stock=stock, user=cls.user2,
                                               entry_quantity=10,
                                               order_type='B', price=500,
                                               is_active=True)
        cls.trade1 = Trade.objects.create(stock=stock, seller=cls.admin,
                                          buyer=cls.user, unit_price=500,
                                          seller_offer=admin_sell_offer,
                                          buyer_offer=user_buy_offer,
                                          quantity=10)
        cls.trade2 = Trade.objects.create(stock=stock, seller=cls.admin,
                                          buyer=cls.user2, unit_price=500,
                                          seller_offer=admin_sell_offer,
                                          buyer_offer=user2_buy_offer,
                                          quantity=10)

    def test_get_trades_list(self):
        trades_quantity = Trade.objects.filter(
            Q(seller=self.user) | Q(buyer=self.user)).count()
        url = reverse('trades-list')
        view = TradeViewSet.as_view({'get': 'list'})
        request = self.factory.get(url)
        force_authenticate(request, self.user, token=self.jwt_token)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), trades_quantity)

    def test_get_list_not_auth_user(self):
        url = reverse('trades-list')
        view = TradeViewSet.as_view({'get': 'list'})
        request = self.factory.get(url)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_stock_list_by_not_auth_user(self):
        url = reverse('trades-list')
        view = TradeViewSet.as_view({'get': 'list'})
        request = self.factory.get(url)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_existing_trade(self):
        url = reverse('trades-detail', kwargs={"pk": self.trade1.pk})
        view = TradeViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(url)
        force_authenticate(request, self.user, token=self.jwt_token)
        response = view(request, pk=self.trade1.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.trade1.id)

    def test_retrieve_not_user_trade(self):
        url = reverse('trades-detail', kwargs={"pk": self.trade2.pk})
        view = TradeViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(url)
        force_authenticate(request, self.user, token=self.jwt_token)
        response = view(request, pk=self.trade2.pk)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_not_auth_user(self):
        url = reverse('trades-detail', kwargs={"pk": self.trade1.pk})
        view = TradeViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(url)
        response = view(request, pk=self.trade1.pk)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
