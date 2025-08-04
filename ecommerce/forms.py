from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Pedido, Produto, Cliente

class PedidoForm(forms.ModelForm):
    """
    Formulário para a criação de um pedido.
    Este formulário inclui um campo para selecionar múltiplos produtos.
    """
    produtos = forms.ModelMultipleChoiceField(
        queryset=Produto.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Selecione os Produtos"
    )

    class Meta:
        model = Pedido
        fields = ['cliente', 'status']

class CadastroForm(UserCreationForm):
    telefone = forms.CharField(max_length=15, required=False, label='Telefone')
    endereco = forms.CharField(widget=forms.Textarea, required=False, label='Endereço')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('telefone', 'endereco',)

    def save(self, commit=True):
        user = super().save(commit)
        telefone = self.cleaned_data.get('telefone')
        endereco = self.cleaned_data.get('endereco')
        # Cria o Cliente vinculado ao novo usuário
        Cliente.objects.create(user=user, telefone=telefone, endereco=endereco)
        return user