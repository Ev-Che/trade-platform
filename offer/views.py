from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Offer
from .permissions import IsOwner
from .serializers import BaseOfferSerializer, \
    CreateUpdateDetailOfferSerializer


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()

    serializers = {
        'retrieve': CreateUpdateDetailOfferSerializer,
        'create': CreateUpdateDetailOfferSerializer,
        'update': CreateUpdateDetailOfferSerializer,
        'partial_update': CreateUpdateDetailOfferSerializer,
        'default': BaseOfferSerializer
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
