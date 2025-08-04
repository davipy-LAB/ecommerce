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
    home
)

urlpatterns = [
    # URLs para a página inicial e autenticação
    path('', home, name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('cadastro/', CadastroView.as_view(), name='cadastro'), # Adicione esta linha
    
    # URLs para o CRUD de Produtos
    path('produtos/', ProdutoListView.as_view(), name='produto_list'),
    path('produtos/novo/', ProdutoCreateView.as_view(), name='produto_create'),
    path('produtos/<int:pk>/editar/', ProdutoUpdateView.as_view(), name='produto_update'),
    path('produtos/<int:pk>/excluir/', ProdutoDeleteView.as_view(), name='produto_delete'),
    
    # URLs para o CRUD de Clientes
    path('clientes/', ClienteListView.as_view(), name='cliente_list'),
    path('clientes/novo/', ClienteCreateView.as_view(), name='cliente_create'),
    path('clientes/<int:pk>/editar/', ClienteUpdateView.as_view(), name='cliente_update'),
    path('clientes/<int:pk>/excluir/', ClienteDeleteView.as_view(), name='cliente_delete'),
    
    # URLs para o CRUD de Pedidos
    path('pedidos/', PedidoListView.as_view(), name='pedido_list'),
    path('pedidos/novo/', PedidoCreateView.as_view(), name='pedido_create'),
    path('pedidos/<int:pk>/', PedidoDetailView.as_view(), name='pedido_detail'),
    path('pedidos/<int:pk>/excluir/', PedidoDeleteView.as_view(), name='pedido_delete'),
]

