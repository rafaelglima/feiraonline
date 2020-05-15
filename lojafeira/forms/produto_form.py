from django.forms import ModelForm
from django import forms
from ..models import Produto

from upload_validator import FileTypeValidator


class ProdutoForm(ModelForm):
    imagem = forms.FileField(
        validators=[FileTypeValidator(
            allowed_types=['image/jpeg', 'image/png']
        )]
    )

    class Meta:
        model = Produto
        fields = ['nome', 'categoria', 'feirante', 'descricao', 'valor', 'valor_promocional', 'unidade_medida',
                  'qtd_estoque', 'imagem']
        exclude = ('feirante',)


class ProdutoFormAdmin(ModelForm):
    imagem = forms.FileField(
        validators=[FileTypeValidator(
            allowed_types=['image/jpeg', 'image/png']
        )]
    )

    class Meta:
        model = Produto
        fields = ['nome', 'categoria', 'feirante', 'descricao', 'valor', 'valor_promocional', 'unidade_medida',
                  'qtd_estoque', 'imagem']
