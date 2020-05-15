from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from lojafeira.models import *
from lojafeira.forms.feirante_form import FeiranteForm


@user_passes_test(lambda u: u.is_superuser)
def cadastrar_feirante(request):
    if request.method == "POST":
        form = FeiranteForm(request.POST, request.FILES)
        if form.is_valid():
            nome = form.cleaned_data["nome"]
            email = form.cleaned_data["email"]
            telefone = form.cleaned_data["telefone"]
            observacao = form.cleaned_data["observacao"]
            imagem = request.FILES['imagem']

            feirante_novo = Feirante(nome=nome, email=email,
                                     telefone=telefone, observacao=observacao, imagem=imagem)
            feirante_novo.save()

            return redirect('listar_feirantes')
    else:
        form = FeiranteForm()
    return render(request, 'lojafeira/painel/feirante/form_feirante.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser)
def listar_feirantes(request):
    # Busca do termo
    if request.method == "GET":
        termo = request.GET.get('termo', None)

        if termo:
            lista_feirantes = Feirante.objects.filter(nome__icontains=termo) | \
                              Feirante.objects.filter(email__icontains=termo) | \
                              Feirante.objects.filter(observacao__icontains=termo)
        else:
            lista_feirantes = Feirante.objects.all()
    else:
        lista_feirantes = Feirante.objects.all()

    # Paginacao de resultados
    page = request.GET.get('page', 1)
    paginator = Paginator(lista_feirantes,
                          3)  # TODO: adicionar na pag de listagem a possibilidade de definir a qtd de registros mostrados
    try:
        feirantes = paginator.page(page)
    except PageNotAnInteger:
        feirantes = paginator.page(1)
    except EmptyPage:
        feirantes = paginator.page(paginator.num_pages)

    return render(request, 'lojafeira/painel/feirante/listar.html', {'dados': feirantes})


@user_passes_test(lambda u: u.is_superuser)
def editar_feirante(request, id):
    feirante = Feirante.objects.get(pk=id)
    form = FeiranteForm(request.POST or None, request.FILES or None, instance=feirante)
    dados = {}

    if request.method == "POST":
        if form.is_valid():
            nome = form.cleaned_data["nome"]
            email = form.cleaned_data["email"]
            telefone = form.cleaned_data["telefone"]
            observacao = form.cleaned_data["observacao"]

            if 'imagem' in request.FILES:
                imagem = request.FILES['imagem']
                feirante.imagem = imagem

            feirante.nome = nome
            feirante.email = email
            feirante.telefone = telefone
            feirante.observacao = observacao

            # Força a atualização para não criar um novo feirante e sim atualizar
            feirante.save(force_update=True)

            dados['status'] = True
            dados['form'] = form
            return render(request, 'lojafeira/painel/feirante/form_feirante.html', dados)
        else:
            dados['status'] = False

    dados['form'] = form
    return render(request, 'lojafeira/painel/feirante/form_feirante.html', dados)


@user_passes_test(lambda u: u.is_superuser)
def remover_feirante(request, id):
    feirante = Feirante.objects.get(pk=id)
    if request.method == 'POST' or request.method == 'GET':
        feirante.delete()
        return redirect('listar_feirantes')
