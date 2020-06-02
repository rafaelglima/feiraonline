from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from lojafeira.manager import UsuarioManager
from django.db.models.signals import m2m_changed


# Create your models here.


class Feirante(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True, null=False, blank=False)
    telefone = models.CharField(max_length=15, null=False, blank=False)
    observacao = models.TextField(null=True, blank=True)
    imagem = models.ImageField(upload_to='feirantes/', null=True)
    dt_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Feirantes'

    def __str__(self):
        return self.nome


class Usuario(AbstractBaseUser, PermissionsMixin):
    objects = UsuarioManager()
    nome = models.CharField(max_length=100, null=False, blank=False)
    sobrenome = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    pais_origem = models.CharField(max_length=20, null=False, blank=False)
    feirante = models.ForeignKey(Feirante, null=True, blank=True,
                                 on_delete=models.SET_NULL)  # feirante é o cliente do Feira Online (PF ou PJ)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'sobrenome', 'pais_origem']

    def __str__(self):
        return self.email


class Categoria(models.Model):
    nome = models.CharField(max_length=50, null=False, blank=False)
    descricao = models.CharField(max_length=100, null=False, blank=False)
    dt_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categorias'
        ordering = ['-nome']

    def __str__(self):
        return self.nome


class Produto(models.Model):
    MEDIDA_CHOICES = (
        ("Un", "Unidade"),
        ("Gr", "Gramas"),
        ("Kg", "Kilogramas"),
        ("Ml", "ML"),
        ("Lt", "Litros"),
    )

    nome = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, null=True, blank=True, on_delete=models.SET_NULL)
    feirante = models.ForeignKey(Feirante, on_delete=models.CASCADE)
    descricao = models.TextField(null=True, blank=True)
    valor = models.DecimalField(max_digits=7, decimal_places=2)  # or FloatField
    valor_promocional = models.DecimalField(max_digits=7, decimal_places=2)
    is_promo = models.BooleanField(default=False)
    unidade_medida = models.CharField(max_length=2, choices=MEDIDA_CHOICES, blank=False, null=False, default="U")
    qtd_estoque = models.IntegerField(blank=False, null=False, default=1)
    imagem = models.ImageField(upload_to='produtos/', null=True)
    dt_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return self.nome


class Pedido(models.Model):
    STATUS_CHOICES = (
        ("A", "Aguardando"),
        ("P", "Preparando"),
        ("D", "Disponível no local"),
        ("E", "Saiu para entrega"),
    )
    # id_pedido = models.AutoField(primary_key=True) # caso deseje alterar o nome da chave primária do model
    feirante = models.ForeignKey("Feirante", on_delete=models.SET_NULL, null=True)
    dt_criacao = models.DateTimeField(auto_now_add=False, default=timezone.now)
    valor = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="A", blank=False, null=False)
    observacao = models.TextField(null=True, blank=True)
    produtos = models.ManyToManyField(Produto, through="PedidoProdutos")

    class Meta:
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        return str(self.id).zfill(5) + '  -  ' + self.feirante.nome


class PedidoProdutos(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, null=True)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, null=True)
    quantidade = models.IntegerField(blank=False, null=False, default=1)

    def __str__(self):
        return self.produto.nome


# Atualizar total do pedido (ao adicionar novo produto, ou remover produto, ou depois de limpar a lista de produtos)
def pre_save_produto_receiver(sender, instance, action, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        produtos = instance.produtos.all()
        total = 0
        for i in produtos:
            if i.is_promo is True:
                total += i.valor_promocional
            else:
                total += i.valor
        instance.valor = total
        instance.save()


m2m_changed.connect(pre_save_produto_receiver, sender=Pedido.produtos.through)

