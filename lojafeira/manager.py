from django.contrib.auth.models import BaseUserManager


class UsuarioManager(BaseUserManager):
    def create_user(self, nome=None, sobrenome=None, email=None, pais_origem=None, feirante=None, password=None):
        if not email:
            raise ValueError("O usuário precisa de um e-mail")
        usuario = self.model(
            nome=nome,
            sobrenome=sobrenome,
            pais_origem=pais_origem,
            feirante=feirante,
            email=self.normalize_email(email)
        )
        usuario.set_password(password)
        usuario.save()
        return usuario

    def create_superuser(self, nome, sobrenome, pais_origem, email, password):
        usuario = self.create_user(
            nome=nome,
            sobrenome=sobrenome,
            email=email,
            pais_origem=pais_origem        # o super usuario não é vinculado à nenhum feirante
        )
        usuario.is_superuser = True
        usuario.set_password(password)
        usuario.save()
        return usuario
