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
    
@login_required
def home(request):
    """
    Exibe um dashboard com métricas do e-commerce.
    """
    total_produtos = Produto.objects.count()
    total_clientes = Cliente.objects.count()
    total_pedidos = Pedido.objects.count()
    total_itens_vendidos = ItemPedido.objects.aggregate(Sum('quantidade'))['quantidade__sum'] or 0

    context = {
        'total_produtos': total_produtos,
        'total_clientes': total_clientes,
        'total_pedidos': total_pedidos,
        'total_itens_vendidos': total_itens_vendidos,
    }
    return render(request, 'ecommerce/home.html', context)

from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.contrib import messages
# Views para a Loja do Cliente
def loja_produtos(request):
    """
    Exibe a lista de produtos para o cliente.
    """
    produtos = Produto.objects.all()
    context = {'produtos': produtos}
    return render(request, 'ecommerce/loja_produtos.html', context)

def adicionar_ao_carrinho(request, produto_id):
    """
    Adiciona um produto ao carrinho (sessão).
    """
    produto = get_object_or_404(Produto, id=produto_id)
    carrinho = request.session.get('carrinho', {})

    if str(produto_id) in carrinho:
        carrinho[str(produto_id)]['quantidade'] += 1
    else:
        carrinho[str(produto_id)] = {
            'nome': produto.nome,
            'preco': str(produto.preco),
            'quantidade': 1,
            'imagem_url': produto.imagem.url if produto.imagem else ''
        }

    request.session['carrinho'] = carrinho
    messages.success(request, f'"{produto.nome}" foi adicionado ao seu carrinho!')
    return redirect('loja_produtos')

def carrinho(request):
    """
    Exibe o conteúdo do carrinho.
    """
    carrinho_itens = request.session.get('carrinho', {})
    total = sum(float(item['preco']) * item['quantidade'] for item in carrinho_itens.values())
    context = {'carrinho_itens': carrinho_itens, 'total': total}
    return render(request, 'ecommerce/carrinho.html', context)

def limpar_carrinho(request):
    """
    Remove todos os itens do carrinho.
    """
    if 'carrinho' in request.session:
        del request.session['carrinho']
        messages.info(request, 'Seu carrinho foi limpo com sucesso!')
    return redirect('carrinho')

@login_required
def checkout_pedido(request):
    """
    Processa a finalização da compra, criando um pedido no banco de dados.
    """
    carrinho_itens = request.session.get('carrinho', {})
    if not carrinho_itens:
        messages.warning(request, 'Seu carrinho está vazio. Adicione itens antes de finalizar a compra.')
        return redirect('carrinho')

    try:
        # Encontra o cliente logado
        cliente = Cliente.objects.get(user=request.user)

        # Cria um novo pedido
        novo_pedido = Pedido.objects.create(cliente=cliente)

        # Adiciona os itens do carrinho ao pedido e atualiza o estoque
        for produto_id, item_data in carrinho_itens.items():
            produto = Produto.objects.get(id=produto_id)
            quantidade = item_data['quantidade']
            
            # Checa se há estoque disponível
            if produto.estoque < quantidade:
                messages.error(request, f'Produto "{produto.nome}" não tem estoque suficiente.')
                return redirect('carrinho')

            # Cria o item do pedido
            ItemPedido.objects.create(
                pedido=novo_pedido,
                produto=produto,
                quantidade=quantidade
            )
            
            # Atualiza o estoque do produto
            produto.estoque -= quantidade
            produto.save()

        # Limpa o carrinho da sessão
        del request.session['carrinho']
        messages.success(request, 'Seu pedido foi realizado com sucesso!')
        return redirect('pedido_confirmacao', pedido_id=novo_pedido.id)

    except Cliente.DoesNotExist:
        messages.error(request, 'Erro: Cliente não encontrado. Por favor, complete seu cadastro.')
        return redirect('cadastro')
    except Exception as e:
        messages.error(request, f'Ocorreu um erro ao finalizar o pedido: {e}')
        return redirect('carrinho')

def pedido_confirmacao(request, pedido_id):
    """
    Exibe a página de confirmação do pedido.
    """
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'ecommerce/pedido_confirmacao.html', {'pedido': pedido})