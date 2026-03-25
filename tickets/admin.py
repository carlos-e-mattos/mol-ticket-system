from django.contrib import admin
from .models import Cliente, Ticket

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'ativo')
    list_filter = ('ativo',)
    search_fields = ('nome', 'email')
    list_editable = ('ativo',)

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'status', 'prioridade', 'cliente', 'criado_em')
    list_filter = ('status', 'prioridade', 'cliente__ativo')
    search_fields = ('titulo', 'cliente__email', 'cliente__nome')
    readonly_fields = ('criado_em', 'atualizado_em')
    autocomplete_fields = ('cliente',)
    date_hierarchy = 'criado_em'
    fieldsets = (
        ('Informações Principais', {
            'fields': ('titulo', 'descricao', 'cliente')
        }),
        ('Status e Prioridade', {
            'fields': ('status', 'prioridade')
        }),
        ('Timestamps', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )