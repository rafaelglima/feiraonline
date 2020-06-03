from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from lojafeira.models import *
from lojafeira.forms.pedido_form import PedidoFormCad, PedidoFormCadAdmin, PedidoFormEdit
from decimal import Decimal


@login_required(login_url='logar_usuario')
def cadastrar_pedido(request):
    dados = {}
    user_feirante_id = Feirante.objects.get(pk=request.user.id).id

    if request.method == "POST":
        if request.user.is_superuser:
            feirante_id = request.POST['feirante']

            form = PedidoFormCadAdmin(data=request.POST, feirante_id=feirante_id, initial={'feirante': feirante_id})
            produtos = Produto.objects.filter(feirante__id=feirante_id)
            if request.POST['selecionou'] == '1':
                dados['form'] = form
                dados['produtos'] = produtos
                return render(request, 'lojafeira/painel/pedido/cadastrar_pedido.html', dados)

        else:
            form = PedidoFormCad(data=request.POST, feirante_id=user_feirante_id)

        if form.is_valid():
            if request.user.is_superuser:
                feirante = form.cleaned_data["feirante"]
            else:
                feirante = Feirante.objects.get(pk=request.user.id)

            observacao = form.cleaned_data["observacao"]
            produtos = form.cleaned_data["produtos"]

            pedido_novo = Pedido.objects.create(feirante=feirante, observacao=observacao)

            for produto in produtos:
                pedido_novo.produtos.add(produto)

            pedido_novo.save()

            return redirect('../cadastrar_pedido_produtos/' + str(pedido_novo.id))

    else:
        if request.user.is_superuser:
            form = PedidoFormCadAdmin(feirante_id=user_feirante_id, initial={'feirante': user_feirante_id})
            produtos = Produto.objects.filter(feirante__id=user_feirante_id)

        else:
            form = PedidoFormCad(feirante_id=user_feirante_id)
            produtos = Produto.objects.filter(feirante__id=user_feirante_id)

    dados['form'] = form
    dados['produtos'] = produtos
    return render(request, 'lojafeira/painel/pedido/cadastrar_pedido.html', dados)


@login_required(login_url='logar_usuario')
def cadastrar_pedido_produtos(request, pedido_id):
    dados = {}
    pedido = Pedido.objects.get(pk=pedido_id)
    pedido_produtos = PedidoProdutos.objects.filter(pedido=pedido_id)

    if request.method == "POST":
        qtd_produtos = request.POST.getlist('qtd_produtos[]')

        count = 0
        pedido.valor = 0.0
        for i in pedido_produtos:
            qtd_anterior = i.quantidade  # variavel auxiliar
            i.quantidade = qtd_produtos[count]

            # Verifica se o produto está em promocao e atualiza valor do pedido
            if i.produto.is_promo is True:
                pedido.valor = Decimal(pedido.valor) + Decimal(i.quantidade) * i.produto.valor_promocional
            else:
                pedido.valor = Decimal(pedido.valor) + Decimal(i.quantidade) * i.produto.valor

            # Atualiza valor no estoque (se aumentarmos qtd no pedido diminui no estoque)
            if int(i.quantidade) > int(qtd_anterior):
                i.produto.qtd_estoque = int(i.produto.qtd_estoque) - (int(i.quantidade) - int(qtd_anterior))
            else:
                i.produto.qtd_estoque = int(i.produto.qtd_estoque) + (int(qtd_anterior) - int(i.quantidade))

            count += 1
            i.produto.save(force_update=True)   # salva estoque novo do produto
            i.save(force_update=True)           # salva quantidade nova dos produtos no pedido

        # Salva valor do pedido (devido a alteração de quantidade de produtos e consequentemente de valor)
        pedido.save(force_update=True)

        dados['status'] = True
        dados['pedido_id'] = pedido.id
        dados['feirante_nome'] = pedido.feirante.nome
        dados['valor'] = pedido.valor
        dados['pedido_produtos'] = pedido_produtos
        return render(request, 'lojafeira/painel/pedido/cadastrar_pedido_produtos.html', dados)

    dados['pedido_id'] = pedido.id
    dados['feirante_nome'] = pedido.feirante.nome
    dados['valor'] = pedido.valor
    dados['pedido_produtos'] = pedido_produtos
    return render(request, 'lojafeira/painel/pedido/cadastrar_pedido_produtos.html', dados)


@login_required(login_url='logar_usuario')
def listar_pedidos(request):
    # Busca do termo
    if request.method == "GET":
        termo = request.GET.get('termo', None)

        if termo:
            if request.user.is_superuser:
                lista_pedidos = Pedido.objects.filter(id__icontains=termo) | \
                                Pedido.objects.filter(feirante__nome__icontains=termo) | \
                                Pedido.objects.filter(observacao__icontains=termo)
            else:
                lista_pedidos = Pedido.objects.filter(id__icontains=termo) | \
                                Pedido.objects.filter(observacao__icontains=termo) | \
                                Pedido.objects.filter(feirante__nome__icontains=termo) | \
                                Pedido.objects.filter(feirante__id=Feirante.objects.get(pk=request.user.id).id)
        else:
            if request.user.is_superuser:
                lista_pedidos = Pedido.objects.all()
            else:
                lista_pedidos = Pedido.objects.filter(feirante__id=Feirante.objects.get(pk=request.user.id).id)
    else:
        if request.user.is_superuser:
            lista_pedidos = Pedido.objects.all()
        else:
            lista_pedidos = Pedido.objects.filter(feirante__id=Feirante.objects.get(pk=request.user.id).id)

    # Paginacao de resultados
    page = request.GET.get('page', 1)
    paginator = Paginator(lista_pedidos,
                          6)  # TODO: adicionar na pag de listagem a possibilidade de definir a qtd de registros mostrados
    try:
        pedidos = paginator.page(page)
    except PageNotAnInteger:
        pedidos = paginator.page(1)
    except EmptyPage:
        pedidos = paginator.page(paginator.num_pages)

    return render(request, 'lojafeira/painel/pedido/listar.html', {'dados': pedidos})


@login_required(login_url='logar_usuario')
def editar_pedido(request, id):
    dados = {}
    pedido = Pedido.objects.get(pk=id)
    feirante = Feirante.objects.get(pk=pedido.feirante.id)
    user_feirante_id = Feirante.objects.get(pk=request.user.id).id
    feirante_id = pedido.feirante.id

    # Questao de seguranca para nao aceitar que usuarios comuns editem pedidos de outros feirantes
    if request.user.is_superuser is False and user_feirante_id != feirante_id:
        return redirect('listar_pedidos')

    if request.method == "POST":
        form = PedidoFormEdit(data=request.POST or None, feirante_id=feirante_id, instance=pedido)

        if form.is_valid():
            observacao = form.cleaned_data["observacao"]
            status = form.cleaned_data["status"]
            produtos = form.cleaned_data["produtos"]

            pedido.observacao = observacao
            pedido.status = status
            pedido.produtos.set(produtos)

            # Força a atualização para não criar um novo pedido e sim atualizar
            pedido.save(force_update=True)

            dados['status'] = True
            dados['form'] = form
            dados['pedido_id'] = pedido.id
            dados['dt_criacao'] = pedido.dt_criacao
            dados['valor'] = pedido.valor
            dados['feirante_nome'] = feirante.nome
            # return render(request, 'lojafeira/painel/pedido/editar_pedido.html', dados)
            return redirect('../../cadastrar_pedido_produtos/' + str(pedido.id))
        else:
            dados['status'] = False

    else:
        form = PedidoFormEdit(feirante_id=feirante_id, instance=pedido)

    dados['form'] = form
    dados['pedido_id'] = pedido.id
    dados['dt_criacao'] = pedido.dt_criacao
    dados['valor'] = pedido.valor
    dados['feirante_nome'] = feirante.nome

    return render(request, 'lojafeira/painel/pedido/editar_pedido.html', dados)


@login_required(login_url='logar_usuario')
def remover_pedido(request, id):
    pedido = Pedido.objects.get(pk=id)
    pedido_produtos = PedidoProdutos.objects.filter(pedido=id)

    if request.method == 'POST' or request.method == 'GET':
        # Atualiza o valor de estoque do produto para entao apagar o pedido
        for pp in pedido_produtos:
            produto = Produto.objects.get(pk=pp.produto.id)
            produto.qtd_estoque = produto.qtd_estoque + pp.quantidade
            produto.save(force_update=True)

        pedido.delete()
        return redirect('listar_pedidos')
