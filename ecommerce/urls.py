from django.urls import path
from .views import (
    ProdutoListView, 
    ProdutoCreateView, 
    ProdutoUpdateView, 
    ProdutoDeleteView,
    ClienteListView,
    ClienteCreateView,
    ClienteUpdateView,
    ClienteDeleteView,
    PedidoListView,
    PedidoDetailView,
    PedidoCreateView,
    PedidoDeleteView,
    CustomLoginView,
    CadastroView,
    LogoutView,
    home,
    loja_produtos,
    adicionar_ao_carrinho,
    carrinho,
    limpar_carrinho, # Adicione esta view
    checkout_pedido, # Adicione esta view
    pedido_confirmacao, # Adicione esta view
)

urlpatterns = [
    # URLs para a página inicial e autenticação
    path('', home, name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('cadastro/', CadastroView.as_view(), name='cadastro'),
    
    # URLs para o CRUD de Produtos (Painel Administrativo)
    path('produtos/', ProdutoListView.as_view(), name='produto_list'),
    path('produtos/novo/', ProdutoCreateView.as_view(), name='produto_create'),
    path('produtos/<int:pk>/editar/', ProdutoUpdateView.as_view(), name='produto_update'),
    path('produtos/<int:pk>/excluir/', ProdutoDeleteView.as_view(), name='produto_delete'),
    
    # URLs para o CRUD de Clientes (Painel Administrativo)
    path('clientes/', ClienteListView.as_view(), name='cliente_list'),
    path('clientes/novo/', ClienteCreateView.as_view(), name='cliente_create'),
    path('clientes/<int:pk>/editar/', ClienteUpdateView.as_view(), name='cliente_update'),
    path('clientes/<int:pk>/excluir/', ClienteDeleteView.as_view(), name='cliente_delete'),
    
    # URLs para o CRUD de Pedidos (Painel Administrativo)
    path('pedidos/', PedidoListView.as_view(), name='pedido_list'),
    path('pedidos/novo/', PedidoCreateView.as_view(), name='pedido_create'),
    path('pedidos/<int:pk>/', PedidoDetailView.as_view(), name='pedido_detail'),
    path('pedidos/<int:pk>/excluir/', PedidoDeleteView.as_view(), name='pedido_delete'),

    # URLs para a Loja do Cliente (Público)
    path('loja/', loja_produtos, name='loja_produtos'),
    path('loja/adicionar/<int:produto_id>/', adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('loja/carrinho/', carrinho, name='carrinho'),
    path('loja/carrinho/limpar/', limpar_carrinho, name='limpar_carrinho'), # Adicione esta linha
    path('loja/checkout/', checkout_pedido, name='checkout_pedido'), # Adicione esta linha
    path('loja/checkout/confirmacao/<int:pedido_id>/', pedido_confirmacao, name='pedido_confirmacao'), # Adicione esta linha
]
