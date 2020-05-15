from django.urls import path
from django.contrib import admin
from .views.feirante_view import *
from .views.usuario_view import *
from .views.produto_view import *
from .views.categoria_view import *

from djangofeira import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('login/', logar_usuario, name='logar_usuario'),
    path('painel/', painel, name='painel'),

    path('painel/listar_usuarios/', listar_usuarios, name='listar_usuarios'),
    path('painel/cadastrar_usuario/', cadastrar_usuario, name='cadastrar_usuario'),
    path('painel/editar_usuario/<int:id>/', editar_usuario, name='editar_usuario'),
    path('painel/remover_usuario/<int:id>/', remover_usuario, name='remover_usuario'),
    path('painel/deslogar_usuario/', deslogar_usuario, name='deslogar_usuario'),
    path('painel/alterar_senha/', alterar_senha, name='alterar_senha'),

    path('painel/listar_feirantes/', listar_feirantes, name='listar_feirantes'),
    path('painel/cadastrar_feirante/', cadastrar_feirante, name='cadastrar_feirante'),
    path('painel/editar_feirante/<int:id>/', editar_feirante, name='editar_feirante'),
    path('painel/remover_feirante/<int:id>/', remover_feirante, name='remover_feirante'),

    path('painel/listar_categorias/', listar_categorias, name='listar_categorias'),
    path('painel/cadastrar_categoria/', cadastrar_categoria, name='cadastrar_categoria'),
    path('painel/editar_categoria/<int:id>/', editar_categoria, name='editar_categoria'),
    path('painel/remover_categoria/<int:id>/', remover_categoria, name='remover_categoria'),

    path('painel/listar_produtos/', listar_produtos, name='listar_produtos'),
    path('painel/cadastrar_produto/', cadastrar_produto, name='cadastrar_produto'),
    path('painel/editar_produto/<int:id>/', editar_produto, name='editar_produto'),
    path('painel/remover_produto/<int:id>/', remover_produto, name='remover_produto'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

