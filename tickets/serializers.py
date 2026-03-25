from rest_framework import serializers
from .models import Cliente, Ticket

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nome', 'email', 'ativo']

class TicketSerializer(serializers.ModelSerializer):
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    prioridade_display = serializers.CharField(source='get_prioridade_display', read_only=True)

    class Meta:
        model = Ticket
        fields = [
            'id', 'titulo', 'descricao',
            'status', 'status_display',
            'prioridade', 'prioridade_display',
            'cliente', 'cliente_nome',
            'criado_em', 'atualizado_em',
        ]
        read_only_fields = ['criado_em', 'atualizado_em']