from django.forms import ModelForm
from django import forms
from ..models import Feirante

from upload_validator import FileTypeValidator


class FeiranteForm(ModelForm):
    foto = forms.FileField(
        validators=[FileTypeValidator(
            allowed_types=['image/jpeg', 'image/png']
        )]
    )

    class Meta:
        model = Feirante
        fields = ['nome', 'sobrenome', 'email', 'cpf', 'descricao', 'foto']
