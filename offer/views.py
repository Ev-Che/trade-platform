from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Offer
from .serializers import OfferSerializer


class OfferViewSet(viewsets.ModelViewSet):
    serializer_class = OfferSerializer
    queryset = Offer.objects.all()
    permission_classes = [IsAuthenticated]
