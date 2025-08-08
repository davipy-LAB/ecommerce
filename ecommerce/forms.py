from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Pedido, Produto


from .models import Cliente

class CadastroForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('cargo',)

    def save(self, commit=True):
        user = super().save(commit)
        # Cria o Cliente apenas se o cargo for 'user'
        if user.cargo == 'user':
            Cliente.objects.create(user=user)
        return user
class PedidoForm(forms.ModelForm):
    # Adicionei um exemplo de campos para um Pedido.
    # Você pode personalizar conforme a necessidade do seu projeto.
    class Meta:
        model = Pedido
        fields = ['cliente']
