from django.forms import ModelForm
from django import forms
from ..models import Categoria


class CategoriaForm(ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'descricao']
