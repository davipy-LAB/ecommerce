from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Nota: Para usar o ImageField com Cloudinary, você precisará instalar as bibliotecas
# `Pillow` (para manipulação de imagens) e `django-cloudinary-storage`.
# A configuração do Cloudinary será feita no settings.py.

class Cliente(models.Model):
    """
    Modelo que representa um cliente no sistema.
    """
    # Relação um-para-um com o modelo de usuário do Django
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Informações adicionais do cliente
    telefone = models.CharField(max_length=15, blank=True, null=True)
    endereco = models.TextField(blank=True, null=True)

    def __str__(self):
        """Representação em string do objeto Cliente."""
        return self.user.username

class Produto(models.Model):
    """
    Modelo que representa um produto à venda.
    """
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.PositiveIntegerField()
    # Campo para a imagem. O upload para o Cloudinary será configurado
    # na próxima etapa, usando uma biblioteca externa.
    imagem = models.ImageField(upload_to='produtos/')

    def __str__(self):
        """Representação em string do objeto Produto."""
        return self.nome

class Pedido(models.Model):
    """
    Modelo que representa um pedido de venda.
    """
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data_pedido = models.DateTimeField(default=timezone.now)
    total_pedido = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Campo para o status do pedido, com opções de escolha
    STATUS_CHOICES = (
        ('Pendente', 'Pendente'),
        ('Processando', 'Processando'),
        ('Enviado', 'Enviado'),
        ('Concluido', 'Concluido'),
        ('Cancelado', 'Cancelado'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pendente')

    def __str__(self):
        """Representação em string do objeto Pedido."""
        return f"Pedido de {self.cliente.user.username} - ID: {self.id}"

class ItemPedido(models.Model):
    """
    Modelo intermediário que conecta Pedido e Produto,
    permitindo que um pedido tenha múltiplos produtos com suas quantidades.
    """
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()

    def __str__(self):
        """Representação em string do objeto ItemPedido."""
        return f"{self.quantidade}x {self.produto.nome} no Pedido #{self.pedido.id}"

# Create your models here.
