import django_filters
from rest_framework import viewsets

from .models import Cliente, Ticket
from .serializers import ClienteSerializer, TicketSerializer


class ClienteFilter(django_filters.FilterSet):
    class Meta:
        model = Cliente
        fields = {'ativo': ['exact'], 'email': ['icontains']}

class TicketFilter(django_filters.FilterSet):
    class Meta:
        model = Ticket
        fields = {
            'status': ['exact'],
            'prioridade': ['exact'],
            'cliente': ['exact'],
            'titulo': ['icontains'],
        }

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filterset_class = ClienteFilter
    search_fields = ['nome', 'email']
    ordering_fields = ['nome', 'email']
    ordering = ['nome']

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.select_related('cliente').all()
    serializer_class = TicketSerializer
    filterset_class = TicketFilter
    search_fields = ['titulo', 'cliente__nome', 'cliente__email']
    ordering_fields = ['criado_em', 'prioridade', 'status']
    ordering = ['-criado_em']
