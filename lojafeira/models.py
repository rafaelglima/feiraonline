from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from lojafeira.manager import UsuarioManager


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
    valor = models.DecimalField(max_digits=7, decimal_places=2)
    valor_promocional = models.DecimalField(max_digits=7, decimal_places=2)
    unidade_medida = models.CharField(max_length=2, choices=MEDIDA_CHOICES, blank=False, null=False, default="U")
    qtd_estoque = models.IntegerField(blank=False, null=False, default=1)
    imagem = models.ImageField(upload_to='produtos/', null=True)
    dt_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return self.nome
