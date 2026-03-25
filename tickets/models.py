from django.db import models


class Cliente(models.Model):
    nome = models.CharField('Nome', max_length=200)
    email = models.EmailField('E-mail', unique=True)
    ativo = models.BooleanField('Ativo', default=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} ({self.email})"

class Ticket(models.Model):
    class Status(models.TextChoices):
        NOVO = 'novo', 'Novo'
        EM_ANDAMENTO = 'em_andamento', 'Em andamento'
        RESOLVIDO = 'resolvido', 'Resolvido'

    class Prioridade(models.TextChoices):
        BAIXA = 'baixa', 'Baixa'
        MEDIA = 'media', 'Média'
        ALTA = 'alta', 'Alta'

    titulo = models.CharField('Título', max_length=300)
    descricao = models.TextField('Descrição', blank=True)
    status = models.CharField(
        'Status',
        max_length=20,
        choices=Status.choices,
        default=Status.NOVO,
    )
    prioridade = models.CharField(
        'Prioridade',
        max_length=10,
        choices=Prioridade.choices,
        default=Prioridade.MEDIA,
    )
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name='tickets',
        verbose_name='Cliente',
    )
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'
        ordering = ['-criado_em']

    def __str__(self):
        return f"#{self.pk} - {self.titulo}"

    @property
    def status_badge_class(self):
        mapping = {
            self.Status.NOVO: 'badge-novo',
            self.Status.EM_ANDAMENTO: 'badge-andamento',
            self.Status.RESOLVIDO: 'badge-resolvido',
        }
        return mapping.get(self.status, '')

    @property
    def prioridade_badge_class(self):
        mapping = {
            self.Prioridade.BAIXA: 'badge-baixa',
            self.Prioridade.MEDIA: 'badge-media',
            self.Prioridade.ALTA: 'badge-alta',
        }
        return mapping.get(self.prioridade, '')
