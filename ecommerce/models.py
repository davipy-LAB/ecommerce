from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField


# Crie um modelo de usuário customizado para adicionar o campo 'cargo'
class CustomUser(AbstractUser):
    """
    Modelo de usuário customizado que adiciona um campo para
    definir o cargo do usuário (usuário ou empresa).
    """
    CARGO_CHOICES = [
        ('user', 'Usuário'),
        ('empresa', 'Empresa'),
    ]
    cargo = models.CharField(max_length=10, choices=CARGO_CHOICES, default='user')
    
    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

class Produto(models.Model):
    """
    Representa um produto disponível na loja.
    """
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField(default=0)
    # Altere o campo de imagem para CloudinaryField para upload de imagens
    imagem = CloudinaryField('image', blank=True, null=True)

    def __str__(self):
        return self.nome

class Cliente(models.Model):
    """
    Representa o perfil de um cliente, associado a um CustomUser.
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=15, blank=True)
    endereco = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username

class Pedido(models.Model):
    """
    Representa um pedido feito por um cliente.
    """
    STATUS_CHOICES = [
        ('aguardando_pagamento', 'Aguardando Pagamento'),
        ('processando', 'Processando'),
        ('enviado', 'Enviado'),
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
    ]
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data_pedido = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aguardando_pagamento')

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.user.username}"

class ItemPedido(models.Model):
    """
    Item individual dentro de um pedido, com a quantidade e o preço no momento da compra.
    O campo 'produto' é um ForeignKey. Internamente, o Django criará um campo
    'produto_id' para armazenar a chave primária do produto.
    """
    pedido = models.ForeignKey(Pedido, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    # Adicionando um valor padrão para evitar erros de migração em dados existentes
    preco = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} em Pedido #{self.pedido.id}"
