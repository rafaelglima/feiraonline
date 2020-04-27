from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from lojafeira.manager import UsuarioManager

# Create your models here.

TIPOPESSOA_CHOICES = (
    ("PF", "Pessoa Física"),
    ("PJ", "Jurídica")
)


class Usuario(AbstractBaseUser, PermissionsMixin):
    objects = UsuarioManager()
    nome = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    pais_origem = models.CharField(max_length=20, null=False, blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'pais_origem']

    def __str__(self):
        return self.email


class Feirante(models.Model):
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    email = models.EmailField(unique=True, null=False, blank=False)
    descricao = models.TextField(null=True, blank=True)
    foto = models.ImageField(upload_to='fotos/', null=True)

    # tipo_pessoa = models.CharField(max_length=2, choices=TIPOPESSOA_CHOICES, blank=False, null=False, default="PF")
    cpf = models.CharField(max_length=11, null=True)
    # cnpj = models.CharField(max_length=14, null=True)
    dt_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Feirantes'

    def __str__(self):
        return self.nome + self.sobrenome
