from django import forms
from ..models import Usuario
from django.db.transaction import commit


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('email', 'nome', 'sobrenome', 'pais_origem')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class UsuarioFormPass(forms.ModelForm):
    password1 = forms.CharField(label="Senha", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirme a Senha", widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ('email', 'nome', 'sobrenome', 'pais_origem')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas informadas não são iguais")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
