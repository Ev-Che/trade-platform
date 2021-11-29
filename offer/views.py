from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Offer
from .permissions import IsOwner
from . import serializers


class OfferViewSet(viewsets.ModelViewSet):
    serializers = {
        'list': serializers.ListOfferSerializer,
        'retrieve': serializers.DetailOfferSerializer,
        'create': serializers.CreateUpdateOfferSerializer,
        'update': serializers.CreateUpdateOfferSerializer,
        'partial_update': serializers.CreateUpdateOfferSerializer,
        'default': serializers.BaseOfferSerializer
    }

    permissions = {
        'update': (IsOwner,),
        'partial_update': (IsOwner,),
        'destroy': (IsOwner,),
        'default': (IsAuthenticated,)
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action,
                                    self.serializers['default'])

    def get_permissions(self):
        permission_classes = self.permissions.get(self.action,
                                                  self.permissions['default'])
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queries = {
            'list': Offer.objects.all().select_related('stock', 'user'),
            'retrieve': Offer.objects.all().select_related('stock', 'user'),
            'default': Offer.objects.all()
        }

        return queries.get(self.action, queries['default'])
