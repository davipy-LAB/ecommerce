
from django.db import models
from django.contrib.auth.models import AbstractUser

# Crie um modelo de usuário customizado para adicionar o campo 'cargo'
class CustomUser(AbstractUser):
    CARGO_CHOICES = [
        ('user', 'Usuário'),
        ('empresa', 'Empresa'),
    ]
    cargo = models.CharField(max_length=10, choices=CARGO_CHOICES, default='user')
    
    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField(default=0)
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)

    def __str__(self):
        return self.nome

class Cliente(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=15, blank=False, default='Telefone não informado')
    endereco = models.CharField(max_length=255, blank=False, default='Endereço não informado')

    def __str__(self):
        return self.user.username

class Pedido(models.Model):
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
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} no Pedido #{self.pedido.id}"
