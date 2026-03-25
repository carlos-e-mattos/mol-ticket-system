from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Cliente, Ticket


class ClienteModelTest(TestCase):
    def test_str(self):
        cliente = Cliente(nome='João', email='joao@email.com')
        self.assertEqual(str(cliente), 'João (joao@email.com)')

    def test_email_unico(self):
        Cliente.objects.create(nome='João', email='joao@email.com')
        with self.assertRaises(Exception):
            Cliente.objects.create(nome='João 2', email='joao@email.com')

class TicketModelTest(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(nome='João', email='joao@email.com')

    def test_str(self):
        ticket = Ticket(pk=1, titulo='Problema no login', cliente=self.cliente)
        self.assertEqual(str(ticket), '#1 - Problema no login')

    def test_status_default(self):
        ticket = Ticket.objects.create(titulo='Teste', cliente=self.cliente)
        self.assertEqual(ticket.status, Ticket.Status.NOVO)

    def test_prioridade_default(self):
        ticket = Ticket.objects.create(titulo='Teste', cliente=self.cliente)
        self.assertEqual(ticket.prioridade, Ticket.Prioridade.MEDIA)

    def test_status_badge_class(self):
        ticket = Ticket(status=Ticket.Status.NOVO)
        self.assertEqual(ticket.status_badge_class, 'badge-novo')
        ticket.status = Ticket.Status.EM_ANDAMENTO
        self.assertEqual(ticket.status_badge_class, 'badge-andamento')
        ticket.status = Ticket.Status.RESOLVIDO
        self.assertEqual(ticket.status_badge_class, 'badge-resolvido')

class TicketViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test123')
        self.cliente = Cliente.objects.create(nome='João', email='joao@email.com')
        self.ticket = Ticket.objects.create(
            titulo='Ticket teste',
            cliente=self.cliente,
            status=Ticket.Status.NOVO,
            prioridade=Ticket.Prioridade.MEDIA,
        )

    def test_lista_redireciona_sem_login(self):
        response = self.client.get(reverse('ticket-list'))
        self.assertRedirects(response, '/login/?next=/tickets/')

    def test_lista_com_login(self):
        self.client.login(username='test', password='test123')
        response = self.client.get(reverse('ticket-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ticket teste')

    def test_detalhe(self):
        self.client.login(username='test', password='test123')
        response = self.client.get(reverse('ticket-detail', args=[self.ticket.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ticket teste')

    def test_criar_ticket(self):
        self.client.login(username='test', password='test123')
        response = self.client.post(reverse('ticket-create'), {
            'titulo': 'Novo ticket',
            'descricao': 'Descrição',
            'status': Ticket.Status.NOVO,
            'prioridade': Ticket.Prioridade.ALTA,
            'cliente': self.cliente.pk,
        })
        self.assertRedirects(response, reverse('ticket-list'))
        self.assertTrue(Ticket.objects.filter(titulo='Novo ticket').exists())

    def test_editar_ticket(self):
        self.client.login(username='test', password='test123')
        response = self.client.post(reverse('ticket-update', args=[self.ticket.pk]), {
            'titulo': 'Ticket editado',
            'descricao': '',
            'status': Ticket.Status.EM_ANDAMENTO,
            'prioridade': Ticket.Prioridade.ALTA,
            'cliente': self.cliente.pk,
        })
        self.assertRedirects(response, reverse('ticket-list'))
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.titulo, 'Ticket editado')

    def test_excluir_ticket(self):
        self.client.login(username='test', password='test123')
        response = self.client.post(reverse('ticket-delete', args=[self.ticket.pk]))
        self.assertRedirects(response, reverse('ticket-list'))
        self.assertFalse(Ticket.objects.filter(pk=self.ticket.pk).exists())

    def test_filtro_por_status(self):
        self.client.login(username='test', password='test123')
        Ticket.objects.create(
            titulo='Ticket resolvido',
            cliente=self.cliente,
            status=Ticket.Status.RESOLVIDO,
            prioridade=Ticket.Prioridade.BAIXA,
        )
        response = self.client.get(reverse('ticket-list'), {'status': 'novo'})
        self.assertContains(response, 'Ticket teste')
        self.assertNotContains(response, 'Ticket resolvido')
