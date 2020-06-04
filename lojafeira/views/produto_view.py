from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from lojafeira.models import *
from lojafeira.forms.produto_form import ProdutoForm, ProdutoFormAdmin


@login_required(login_url='logar_usuario')
def cadastrar_produto(request):
    if request.method == "POST":
        if request.user.is_superuser:
            form = ProdutoFormAdmin(request.POST, request.FILES)
        else:
            form = ProdutoForm(request.POST, request.FILES)

        if form.is_valid():
            nome = form.cleaned_data["nome"]
            categoria = form.cleaned_data["categoria"]

            if request.user.is_superuser:
                feirante = form.cleaned_data["feirante"]
            else:
                feirante = Feirante.objects.get(pk=request.user.id)

            descricao = form.cleaned_data["descricao"]
            valor = form.cleaned_data["valor"]
            is_promo = form.cleaned_data["is_promo"]
            valor_promocional = form.cleaned_data["valor_promocional"]
            unidade_medida = form.cleaned_data["unidade_medida"]
            qtd_estoque = form.cleaned_data["qtd_estoque"]
            imagem = request.FILES['imagem']

            produto_novo = Produto(nome=nome, descricao=descricao, categoria=categoria, feirante=feirante,
                                   valor=valor, is_promo=is_promo, valor_promocional=valor_promocional, unidade_medida=unidade_medida,
                                   qtd_estoque=qtd_estoque, imagem=imagem)
            produto_novo.save()

            return redirect('listar_produtos')
    else:
        if request.user.is_superuser:
            form = ProdutoFormAdmin()
        else:
            form = ProdutoForm()
    return render(request, 'lojafeira/painel/produto/form_produto.html', {'form': form})


@login_required(login_url='logar_usuario')
def listar_produtos(request):
    # Busca do termo
    if request.method == "GET":
        termo = request.GET.get('termo', None)

        if termo:
            if request.user.is_superuser:
                lista_produtos = Produto.objects.filter(nome__icontains=termo) | \
                                 Produto.objects.filter(descricao__icontains=termo) | \
                                 Produto.objects.filter(feirante__nome__icontains=termo)
            else:
                lista_produtos = Produto.objects.filter(nome__icontains=termo,
                                                        feirante__id=Usuario.objects.get(pk=request.user.id).feirante.id) | \
                                  Produto.objects.filter(descricao__icontains=termo,
                                                         feirante__id=Usuario.objects.get(pk=request.user.id).feirante.id)

        else:
            if request.user.is_superuser:
                lista_produtos = Produto.objects.all()
            else:
                lista_produtos = Produto.objects.filter(feirante__id=Usuario.objects.get(pk=request.user.id).feirante.id)
    else:
        if request.user.is_superuser:
            lista_produtos = Produto.objects.all()
        else:
            lista_produtos = Produto.objects.filter(feirante__id=Usuario.objects.get(pk=request.user.id).feirante.id)

    # Paginacao de resultados
    page = request.GET.get('page', 1)
    paginator = Paginator(lista_produtos,
                          3)  # TODO: adicionar na pag de listagem a possibilidade de definir a qtd de registros mostrados
    try:
        produtos = paginator.page(page)
    except PageNotAnInteger:
        produtos = paginator.page(1)
    except EmptyPage:
        produtos = paginator.page(paginator.num_pages)

    return render(request, 'lojafeira/painel/produto/listar.html', {'dados': produtos})


@login_required(login_url='logar_usuario')
def editar_produto(request, id):
    produto = Produto.objects.get(pk=id)
    if request.user.is_superuser:
        form = ProdutoFormAdmin(request.POST or None, request.FILES or None, instance=produto)
    else:
        form = ProdutoForm(request.POST or None, request.FILES or None, instance=produto)
    dados = {}

    if request.method == "POST":
        if form.is_valid():
            nome = form.cleaned_data["nome"]
            categoria = form.cleaned_data["categoria"]
            if request.user.is_superuser:
                feirante = form.cleaned_data["feirante"]
            else:
                feirante = Feirante.objects.get(pk=request.user.id)
            descricao = form.cleaned_data["descricao"]
            valor = form.cleaned_data["valor"]
            is_promo = form.cleaned_data["is_promo"]
            valor_promocional = form.cleaned_data["valor_promocional"]
            unidade_medida = form.cleaned_data["unidade_medida"]
            qtd_estoque = form.cleaned_data["qtd_estoque"]

            if 'imagem' in request.FILES:
                imagem = request.FILES['imagem']
                produto.imagem = imagem

            produto.nome = nome
            produto.categoria = categoria
            produto.feirante = feirante
            produto.descricao = descricao
            produto.valor = valor
            produto.is_promo = is_promo
            produto.valor_promocional = valor_promocional
            produto.unidade_medida = unidade_medida
            produto.qtd_estoque = qtd_estoque

            # Força a atualização para não criar um novo produto e sim atualizar
            produto.save(force_update=True)

            dados['status'] = True
            dados['form'] = form
            return render(request, 'lojafeira/painel/produto/form_produto.html', dados)
        else:
            dados['status'] = False

    dados['form'] = form
    return render(request, 'lojafeira/painel/produto/form_produto.html', dados)


@login_required(login_url='logar_usuario')
def remover_produto(request, id):
    produto = Produto.objects.get(pk=id)
    if request.method == 'POST' or request.method == 'GET':
        produto.delete()
        return redirect('listar_produtos')
