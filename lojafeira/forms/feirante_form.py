from django.forms import ModelForm
from django import forms
from ..models import Feirante

from upload_validator import FileTypeValidator


class FeiranteForm(ModelForm):
    imagem = forms.FileField(
        validators=[FileTypeValidator(
            allowed_types=['image/jpeg', 'image/png']
        )]
    )

    class Meta:
        model = Feirante
        fields = ['nome', 'email', 'telefone', 'observacao', 'imagem']
