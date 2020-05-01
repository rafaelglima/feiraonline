from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from lojafeira.models import *
from lojafeira.forms.usuario_form import UsuarioForm, UsuarioFormPass
from lojafeira.forms.login_form import LoginForm


# Create your views here.

def index(request):

    dados = {}
    dados['feirantes'] = Feirante.objects.all()

    return render(request, 'lojafeira/index.html', dados)


@login_required(login_url='logar_usuario')
def painel(request):
    return render(request, 'lojafeira/painel/painel.html')


def logar_usuario(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST or None)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            usuario = authenticate(request, username=username, password=password)
            if usuario is not None:
                login(request, usuario)
                return redirect('painel')
            else:
                form = LoginForm()
    else:
        form = LoginForm()
    return render(request, 'lojafeira/painel/login.html', {'form': form})


@login_required(login_url='logar_usuario')
def deslogar_usuario(request):
    logout(request)
    return redirect('logar_usuario')


@login_required(login_url='logar_usuario')
def alterar_senha(request):
    dados = {}
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # armazena senha criptografada
            dados['status'] = True
            dados['form'] = form
            return render(request, 'lojafeira/painel/usuario/alterar_senha.html', dados)
        else:
            dados['status'] = False
    else:
        form = PasswordChangeForm(request.user)

    dados['form'] = form
    return render(request, 'lojafeira/painel/usuario/alterar_senha.html', dados)


@user_passes_test(lambda u: u.is_superuser)
def cadastrar_usuario(request):
    if request.method == "POST":
        form = UsuarioFormPass(data=request.POST)
        if form.is_valid():
            nome = form.cleaned_data["nome"]
            sobrenome = form.cleaned_data["sobrenome"]
            email = form.cleaned_data["email"]
            pais_origem = form.cleaned_data["pais_origem"]
            password = form.cleaned_data["password1"]

            # chama a função de criação do usuário localizada no manager
            Usuario.objects.create_user(nome=nome, sobrenome=sobrenome, email=email, pais_origem=pais_origem, password=password)

            return redirect('listar_usuarios')
    else:
        form = UsuarioFormPass()
    return render(request, 'lojafeira/painel/usuario/cadastrar.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser)
def listar_usuarios(request):
    if request.method == "GET":
        termo = request.GET.get('termo', None)

        if termo:
            lista_usuarios = Usuario.objects.filter(nome__icontains=termo)

        else:
            lista_usuarios = Usuario.objects.all()
    else:
        lista_usuarios = Usuario.objects.all()

    # lista_usuarios = Usuario.objects.all()

    page = request.GET.get('page', 1)
    paginator = Paginator(lista_usuarios, 3)
    try:
        usuarios = paginator.page(page)
    except PageNotAnInteger:
        usuarios = paginator.page(1)
    except EmptyPage:
        usuarios = paginator.page(paginator.num_pages)

    return render(request, 'lojafeira/painel/usuario/listar.html', {'dados': usuarios})


@user_passes_test(lambda u: u.is_superuser)
def editar_usuario(request, id):
    usuario = Usuario.objects.get(pk=id)
    form = UsuarioForm(request.POST or None, instance=usuario)
    dados = {}

    if request.method == "POST":
        if form.is_valid():
            nome = form.cleaned_data["nome"]
            sobrenome = form.cleaned_data["sobrenome"]
            pais_origem = form.cleaned_data["pais_origem"]

            usuario.nome = nome
            usuario.sobrenome = sobrenome
            usuario.pais_origem = pais_origem

            # Força a atualização para não criar um novo usuário e sim atualizar
            usuario.save(force_update=True)

            dados['status'] = True
            dados['form'] = form
            return render(request, 'lojafeira/painel/usuario/editar.html', dados)
        else:
            dados['status'] = False

    dados['form'] = form
    return render(request, 'lojafeira/painel/usuario/editar.html', dados)


@user_passes_test(lambda u: u.is_superuser)
def remover_usuario(request, id):
    usuario = Usuario.objects.get(pk=id)
    if request.method == 'POST' or request.method == 'GET':
        usuario.delete()
        return redirect('listar_usuarios')
