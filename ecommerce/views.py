from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.db.models import Sum
from django.contrib import messages
from django.http import Http404

from .models import Produto, Cliente, Pedido, ItemPedido, CustomUser
from .forms import PedidoForm, CadastroForm


# Decorator customizado para checar se o usuário é do tipo 'empresa'
def is_empresa(user):
    return user.is_authenticated and user.cargo == 'empresa'

empresa_required = user_passes_test(is_empresa, login_url=reverse_lazy('loja_produtos'))


# Views para o CRUD de Produtos (Área da Empresa)
@method_decorator(empresa_required, name='dispatch')
class ProdutoListView(ListView):
    model = Produto
    template_name = 'ecommerce/produto_list.html'
    context_object_name = 'produtos'

@method_decorator(empresa_required, name='dispatch')
class ProdutoCreateView(CreateView):
    model = Produto
    template_name = 'ecommerce/produto_form.html'
    fields = ['nome', 'descricao', 'preco', 'estoque', 'imagem']
    success_url = reverse_lazy('produto_list')

@method_decorator(empresa_required, name='dispatch')
class ProdutoUpdateView(UpdateView):
    model = Produto
    template_name = 'ecommerce/produto_form.html'
    fields = ['nome', 'descricao', 'preco', 'estoque', 'imagem']
    success_url = reverse_lazy('produto_list')

@method_decorator(empresa_required, name='dispatch')
class ProdutoDeleteView(DeleteView):
    model = Produto
    template_name = 'ecommerce/produto_confirm_delete.html'
    success_url = reverse_lazy('produto_list')

# Views para o CRUD de Clientes (Área da Empresa)
@method_decorator(empresa_required, name='dispatch')
class ClienteListView(ListView):
    model = Cliente
    template_name = 'ecommerce/cliente_list.html'
    context_object_name = 'clientes'

@method_decorator(empresa_required, name='dispatch')
class ClienteCreateView(CreateView):
    model = Cliente
    template_name = 'ecommerce/cliente_form.html'
    fields = ['user', 'telefone', 'endereco']
    success_url = reverse_lazy('cliente_list')

@method_decorator(empresa_required, name='dispatch')
class ClienteUpdateView(UpdateView):
    model = Cliente
    template_name = 'ecommerce/cliente_form.html'
    fields = ['user', 'telefone', 'endereco']
    success_url = reverse_lazy('cliente_list')

@method_decorator(empresa_required, name='dispatch')
class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = 'ecommerce/cliente_confirm_delete.html'
    success_url = reverse_lazy('cliente_list')

# Views para o CRUD de Pedidos (Área da Empresa)
@method_decorator(empresa_required, name='dispatch')
class PedidoListView(ListView):
    model = Pedido
    template_name = 'ecommerce/pedido_list.html'
    context_object_name = 'pedidos'

@method_decorator(empresa_required, name='dispatch')
class PedidoDetailView(DetailView):
    model = Pedido
    template_name = 'ecommerce/pedido_detail.html'
    context_object_name = 'pedido'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obter os itens do pedido para exibir
        context['itens_pedido'] = ItemPedido.objects.filter(pedido=self.object)
        return context

@method_decorator(empresa_required, name='dispatch')
class PedidoCreateView(CreateView):
    model = Pedido
    template_name = 'ecommerce/pedido_form.html'
    fields = ['cliente', 'status']
    success_url = reverse_lazy('pedido_list')

@method_decorator(empresa_required, name='dispatch')
class PedidoDeleteView(DeleteView):
    model = Pedido
    template_name = 'ecommerce/pedido_confirm_delete.html'
    success_url = reverse_lazy('pedido_list')

# Views de autenticação
class CustomLoginView(LoginView):
    template_name = 'ecommerce/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        # Redireciona para a página de produtos se for uma empresa, senão para a loja
        if self.request.user.cargo == 'empresa':
            return reverse_lazy('produto_list')
        return reverse_lazy('loja_produtos')

class CadastroView(SuccessMessageMixin, CreateView):
    form_class = CadastroForm
    success_url = reverse_lazy('login')
    template_name = 'ecommerce/cadastro.html'
    success_message = "Sua conta foi criada com sucesso! Faça o login para continuar."

# Views para a loja
def home(request):
    return render(request, 'ecommerce/home.html')

def loja_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'ecommerce/loja_produtos.html', {'produtos': produtos})

@login_required
def adicionar_ao_carrinho(request, produto_id):
    carrinho = request.session.get('carrinho', {})
    produto = get_object_or_404(Produto, id=produto_id)

    if str(produto_id) in carrinho:
        # Se o produto já está no carrinho, aumenta a quantidade
        carrinho[str(produto_id)]['quantidade'] += 1
    else:
        # Adiciona o produto ao carrinho
        carrinho[str(produto_id)] = {
            'nome': produto.nome,
            'preco': str(produto.preco),
            'quantidade': 1,
            'imagem_url': produto.imagem.url if produto.imagem else None
        }

    request.session['carrinho'] = carrinho
    messages.success(request, f'O produto "{produto.nome}" foi adicionado ao seu carrinho!')
    return redirect('loja_produtos')

@login_required
def remover_do_carrinho(request, produto_id):
    carrinho = request.session.get('carrinho', {})
    produto_id_str = str(produto_id)

    if produto_id_str in carrinho:
        del carrinho[produto_id_str]
        request.session['carrinho'] = carrinho
        messages.success(request, 'Produto removido do carrinho com sucesso!')

    return redirect('carrinho')

@login_required
def carrinho(request):
    carrinho_itens = request.session.get('carrinho', {})
    total = sum(float(item['preco']) * item['quantidade'] for item in carrinho_itens.values())
    return render(request, 'ecommerce/carrinho.html', {'carrinho_itens': carrinho_itens, 'total': total})

@login_required
def limpar_carrinho(request):
    if 'carrinho' in request.session:
        del request.session['carrinho']
        messages.info(request, 'Seu carrinho foi esvaziado.')
    return redirect('loja_produtos')

@login_required
def checkout_pedido(request):
    try:
        # Obter o cliente a partir do usuário logado
        cliente = Cliente.objects.get(user=request.user)
        carrinho_itens = request.session.get('carrinho', {})

        if not carrinho_itens:
            messages.error(request, 'Seu carrinho está vazio.')
            return redirect('carrinho')

        # Criar um novo pedido
        novo_pedido = Pedido.objects.create(cliente=cliente)

        # Adicionar os itens do carrinho ao pedido
        for produto_id, item in carrinho_itens.items():
            produto = get_object_or_404(Produto, pk=produto_id)
            ItemPedido.objects.create(
                pedido=novo_pedido,
                produto=produto,
                quantidade=item['quantidade'],
                preco=item['preco']  # Corrigido aqui: trocado 'preco_unitario' por 'preco'
            )
            # Atualiza o estoque do produto
            produto.estoque -= item['quantidade']
            produto.save()

        # Limpa o carrinho
        del request.session['carrinho']
        messages.success(request, 'Seu pedido foi realizado com sucesso!')
        return redirect('pedido_confirmacao', pedido_id=novo_pedido.id)

    except Cliente.DoesNotExist:
        messages.error(request, 'Erro: Cliente não encontrado. Por favor, complete seu cadastro.')
        return redirect('cadastro')
    except Exception as e:
        messages.error(request, f'Ocorreu um erro ao finalizar o pedido: {e}')
        return redirect('carrinho')

@login_required
def pedido_confirmacao(request, pedido_id):
    """
    Exibe a página de confirmação do pedido.
    """
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'ecommerce/pedido_confirmacao.html', {'pedido': pedido})

@empresa_required
def update_pedido_status(request, pk):
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, pk=pk)
        novo_status = request.POST.get('status')
        if novo_status:
            pedido.status = novo_status
            pedido.save()
            messages.success(request, f'O status do pedido #{pedido.id} foi atualizado para \"{novo_status}\".')
    return redirect('pedido_detail', pk=pk)

@login_required
def meus_pedidos(request):
    """
    Exibe a lista de pedidos do cliente logado.
    """
    # Obter o cliente a partir do usuário logado
    try:
        cliente = Cliente.objects.get(user=request.user)
        pedidos = Pedido.objects.filter(cliente=cliente).order_by('-data_pedido')
    except Cliente.DoesNotExist:
        # Se o usuário não tem um perfil de cliente, retorna uma lista vazia
        pedidos = None
    
    return render(request, 'ecommerce/meus_pedidos.html', {'pedidos': pedidos})
