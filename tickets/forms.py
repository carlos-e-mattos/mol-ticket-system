from django import forms
from .models import Ticket

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['titulo', 'descricao', 'status', 'prioridade', 'cliente']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'prioridade': forms.Select(attrs={'class': 'form-select'}),
            'cliente': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].queryset = self.fields['cliente'].queryset.filter(ativo=True)

class TicketFilterForm(forms.Form):
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buscar por título ou cliente...'}),
        label='Busca',
    )
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'Todos os status')] + list(Ticket.Status.choices),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Status',
    )
    prioridade = forms.ChoiceField(
        required=False,
        choices=[('', 'Todas as prioridades')] + list(Ticket.Prioridade.choices),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Prioridade',
    )