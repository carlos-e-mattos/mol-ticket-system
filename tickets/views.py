from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from .forms import TicketFilterForm, TicketForm
from .models import Ticket

class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'tickets/ticket_list.html'
    context_object_name = 'tickets'
    paginate_by = 10

    def get_queryset(self):
        qs = Ticket.objects.select_related('cliente')
        form = TicketFilterForm(self.request.GET)
        if form.is_valid():
            q = form.cleaned_data.get('q')
            status = form.cleaned_data.get('status')
            prioridade = form.cleaned_data.get('prioridade')
            if q:
                qs = qs.filter(
                    Q(titulo__icontains=q) |
                    Q(cliente__nome__icontains=q) |
                    Q(cliente__email__icontains=q)
                )
            if status:
                qs = qs.filter(status=status)
            if prioridade:
                qs = qs.filter(prioridade=prioridade)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['filter_form'] = TicketFilterForm(self.request.GET)
        return ctx

class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = 'tickets/ticket_detail.html'
    context_object_name = 'ticket'

class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'tickets/ticket_form.html'
    success_url = reverse_lazy('ticket-list')

    def form_valid(self, form):
        messages.success(self.request, 'Ticket criado com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = 'Criar'
        return ctx

class TicketUpdateView(LoginRequiredMixin, UpdateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'tickets/ticket_form.html'
    success_url = reverse_lazy('ticket-list')

    def form_valid(self, form):
        messages.success(self.request, 'Ticket atualizado com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = 'Editar'
        return ctx

class TicketDeleteView(LoginRequiredMixin, DeleteView):
    model = Ticket
    template_name = 'tickets/ticket_confirm_delete.html'
    success_url = reverse_lazy('ticket-list')
    context_object_name = 'ticket'

    def form_valid(self, form):
        messages.success(self.request, 'Ticket excluído com sucesso!')
        return super().form_valid(form)