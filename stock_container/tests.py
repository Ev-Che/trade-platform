import datetime

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import (APITestCase, APIRequestFactory,
                                 force_authenticate)

from .models import Favorite, Inventory
from stock_management.models import Currency, Price, Stock
from .views import FavoritesViewSet, InventoryViewSet

User = get_user_model()


class BaseSetUpClass(APITestCase):

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
        cls.stock = Stock.objects.create(name='test1', code='T1',
                                         price=price)

        price2 = Price.objects.create(currency=currency, value=200,
                                      date_of_change=datetime.datetime.now())
        cls.stock_for_create = Stock.objects.create(name='test2', code='T2',
                                                    price=price2)


class FavoritesViewSetTestCase(BaseSetUpClass):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.favorite = Favorite.objects.create(user=cls.user,
                                               favorite_stock=cls.stock)

    def test_get_favorites_list(self):
        url = reverse('favorite-list')
        objects_before = Favorite.objects.all().count()
        view = FavoritesViewSet.as_view({'get': 'list'})
        request = self.factory.get(url)
        force_authenticate(request, self.user, token=self.jwt_token)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(objects_before, len(response.data))

    def test_create_favorite(self):
        url = reverse('favorite-list')
        data = {'user': self.user.pk,
                'favorite_stock': self.stock_for_create.pk}

        objects_before = Favorite.objects.all().count()

        view = FavoritesViewSet.as_view({'post': 'create'})
        request = self.factory.post(url, data=data)
        force_authenticate(request, self.user, token=self.jwt_token)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(objects_before + 1, Favorite.objects.all().count())

    def test_delete_favorite(self):
        url = reverse('favorite-detail', kwargs={'pk': self.favorite.pk})
        objects_before = Favorite.objects.all().count()
        view = FavoritesViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete(url, pk=self.favorite.pk)

        force_authenticate(request, self.user, token=self.jwt_token)
        response = view(request, pk=self.favorite.pk)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(objects_before - 1, Favorite.objects.all().count())


class InventoryTestCase(BaseSetUpClass):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.inventory = Inventory.objects.create(user=cls.user,
                                                 stock=cls.stock, quantity=10)

    def test_get_inventory_list(self):
        url = reverse('inventory-list')
        objects_before = Inventory.objects.all().count()
        view = InventoryViewSet.as_view({'get': 'list'})
        request = self.factory.get(url)
        force_authenticate(request, self.user, token=self.jwt_token)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(objects_before, len(response.data))
