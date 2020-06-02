from django.forms import ModelForm
from django import forms
from ..models import Pedido
from ..models import Produto
from ..models import Feirante


class PedidoFormCadAdmin(ModelForm):
    feirante = forms.ModelChoiceField(queryset=Feirante.objects.none(),
                                      widget=forms.Select(attrs={'onchange': "submitForm()"}))

    produtos = forms.ModelMultipleChoiceField(queryset=Produto.objects.none())
    # produtos = forms.ModelMultipleChoiceField(queryset=Produto.objects.none(), widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Pedido
        fields = ['feirante', 'observacao', 'produtos']

    def __init__(self, feirante_id, *args, **kwargs):
        super(PedidoFormCadAdmin, self).__init__(*args, **kwargs)

        self.fields['produtos'].queryset = Produto.objects.filter(feirante__id=feirante_id)
        self.fields['feirante'].queryset = Feirante.objects.all()


class PedidoFormCad(ModelForm):
    produtos = forms.ModelMultipleChoiceField(queryset=Produto.objects.none())

    class Meta:
        model = Pedido
        fields = ['observacao', 'produtos']

    def __init__(self, feirante_id, *args, **kwargs):
        super(PedidoFormCad, self).__init__(*args, **kwargs)

        self.fields['produtos'].queryset = Produto.objects.filter(feirante__id=feirante_id)


class PedidoFormEdit(ModelForm):
    produtos = forms.ModelMultipleChoiceField(queryset=Produto.objects.none())
    # produtos = forms.ModelMultipleChoiceField(queryset=Produto.objects.none(), widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Pedido
        fields = ['observacao', 'produtos', 'status']

    def __init__(self, feirante_id, *args, **kwargs):
        super(PedidoFormEdit, self).__init__(*args, **kwargs)

        self.fields['produtos'].queryset = Produto.objects.filter(feirante__id=feirante_id)