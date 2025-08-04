from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Produto, Cliente, Pedido, ItemPedido
from .forms import PedidoForm, CadastroForm # Importamos o novo formulário de cadastro

# Views para o CRUD de Produtos
@method_decorator(login_required, name='dispatch')
class ProdutoListView(ListView):
    model = Produto
    template_name = 'ecommerce/produto_list.html'
    context_object_name = 'produtos'

@method_decorator(login_required, name='dispatch')
class ProdutoCreateView(CreateView):
    model = Produto
    template_name = 'ecommerce/produto_form.html'
    fields = ['nome', 'descricao', 'preco', 'estoque', 'imagem']
    success_url = reverse_lazy('produto_list')

@method_decorator(login_required, name='dispatch')
class ProdutoUpdateView(UpdateView):
    model = Produto
    template_name = 'ecommerce/produto_form.html'
    fields = ['nome', 'descricao', 'preco', 'estoque', 'imagem']
    success_url = reverse_lazy('produto_list')

@method_decorator(login_required, name='dispatch')
class ProdutoDeleteView(DeleteView):
    model = Produto
    template_name = 'ecommerce/produto_confirm_delete.html'
    success_url = reverse_lazy('produto_list')


# Views para o CRUD de Clientes
@method_decorator(login_required, name='dispatch')
class ClienteListView(ListView):
    model = Cliente
    template_name = 'ecommerce/cliente_list.html'
    context_object_name = 'clientes'

@method_decorator(login_required, name='dispatch')
class ClienteCreateView(SuccessMessageMixin, CreateView):
    model = Cliente
    template_name = 'ecommerce/cliente_form.html'
    fields = ['user', 'telefone', 'endereco']
    success_url = reverse_lazy('cliente_list')
    success_message = "Cliente '%(user)s' criado com sucesso!"

@method_decorator(login_required, name='dispatch')
class ClienteUpdateView(SuccessMessageMixin, UpdateView):
    model = Cliente
    template_name = 'ecommerce/cliente_form.html'
    fields = ['user', 'telefone', 'endereco']
    success_url = reverse_lazy('cliente_list')
    success_message = "Cliente '%(user)s' atualizado com sucesso!"

@method_decorator(login_required, name='dispatch')
class ClienteDeleteView(SuccessMessageMixin, DeleteView):
    model = Cliente
    template_name = 'ecommerce/cliente_confirm_delete.html'
    success_url = reverse_lazy('cliente_list')
    success_message = "Cliente '%(user)s' excluído com sucesso!"


# Views para o CRUD de Pedidos de Venda
@method_decorator(login_required, name='dispatch')
class PedidoListView(ListView):
    model = Pedido
    template_name = 'ecommerce/pedido_list.html'
    context_object_name = 'pedidos'

@method_decorator(login_required, name='dispatch')
class PedidoDetailView(DetailView):
    model = Pedido
    template_name = 'ecommerce/pedido_detail.html'
    context_object_name = 'pedido'

@method_decorator(login_required, name='dispatch')
class PedidoCreateView(SuccessMessageMixin, CreateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'ecommerce/pedido_form.html'
    success_url = reverse_lazy('pedido_list')
    success_message = "Pedido #%(id)s criado com sucesso!"
    
    def form_valid(self, form):
        response = super().form_valid(form)
        produtos_selecionados = form.cleaned_data.get('produtos')
        
        for produto in produtos_selecionados:
            ItemPedido.objects.create(
                pedido=self.object,
                produto=produto,
                quantidade=1
            )
        return response

@method_decorator(login_required, name='dispatch')
class PedidoDeleteView(DeleteView):
    model = Pedido
    template_name = 'ecommerce/pedido_confirm_delete.html'
    success_url = reverse_lazy('pedido_list')

# Views de Autenticação e Página Inicial
class CustomLoginView(LoginView):
    template_name = 'ecommerce/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')

class CadastroView(SuccessMessageMixin, CreateView):
    form_class = CadastroForm
    template_name = 'ecommerce/register.html'
    success_url = reverse_lazy('login')
    success_message = "Conta criada com sucesso! Faça login para continuar."
    
def home(request):
    return render(request, 'ecommerce/home.html')
