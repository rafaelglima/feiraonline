from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from lojafeira.models import *
from lojafeira.forms.categoria_form import CategoriaForm


@user_passes_test(lambda u: u.is_superuser)
def cadastrar_categoria(request):
    if request.method == "POST":
        form = CategoriaForm(request.POST, request.FILES)
        if form.is_valid():
            nome = form.cleaned_data["nome"]
            descricao = form.cleaned_data["descricao"]

            categoria_novo = Categoria(nome=nome, descricao=descricao)
            categoria_novo.save()

            return redirect('listar_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'lojafeira/painel/categoria/form_categoria.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser)
def listar_categorias(request):
    # Busca do termo
    if request.method == "GET":
        termo = request.GET.get('termo', None)

        if termo:
            lista_categorias = Categoria.objects.filter(nome__icontains=termo) | \
                              Categoria.objects.filter(descricao__icontains=termo)
        else:
            lista_categorias = Categoria.objects.all()
    else:
        lista_categorias = Categoria.objects.all()

    # Paginacao de resultados
    page = request.GET.get('page', 1)
    paginator = Paginator(lista_categorias, 3)  # TODO: adicionar na pag de listagem a possibilidade de definir a qtd de registros mostrados
    try:
        categorias = paginator.page(page)
    except PageNotAnInteger:
        categorias = paginator.page(1)
    except EmptyPage:
        categorias = paginator.page(paginator.num_pages)

    return render(request, 'lojafeira/painel/categoria/listar.html', {'dados': categorias})


@user_passes_test(lambda u: u.is_superuser)
def editar_categoria(request, id):
    categoria = Categoria.objects.get(pk=id)
    form = CategoriaForm(request.POST or None, instance=categoria)
    dados = {}

    if request.method == "POST":
        if form.is_valid():
            nome = form.cleaned_data["nome"]
            descricao = form.cleaned_data["descricao"]

            categoria.nome = nome
            categoria.descricao = descricao

            # Força a atualização para não criar um novo categoria e sim atualizar
            categoria.save(force_update=True)

            dados['status'] = True
            dados['form'] = form
            return render(request, 'lojafeira/painel/categoria/form_categoria.html', dados)
        else:
            dados['status'] = False

    dados['form'] = form
    return render(request, 'lojafeira/painel/categoria/form_categoria.html', dados)


@user_passes_test(lambda u: u.is_superuser)
def remover_categoria(request, id):
    categoria = Categoria.objects.get(pk=id)
    if request.method == 'POST' or request.method == 'GET':
        categoria.delete()
        return redirect('listar_categorias')