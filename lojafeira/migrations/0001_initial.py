# Generated by Django 3.0.6 on 2020-05-26 02:03

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('descricao', models.CharField(max_length=100)),
                ('dt_criacao', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Categorias',
                'ordering': ['-nome'],
            },
        ),
        migrations.CreateModel(
            name='Feirante',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('telefone', models.CharField(max_length=15)),
                ('observacao', models.TextField(blank=True, null=True)),
                ('imagem', models.ImageField(null=True, upload_to='feirantes/')),
                ('dt_criacao', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Feirantes',
            },
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt_criacao', models.DateTimeField(default=django.utils.timezone.now)),
                ('valor', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('status', models.CharField(choices=[('A', 'Aguardando'), ('P', 'Preparando'), ('D', 'Disponível no local'), ('E', 'Saiu para entrega')], default='A', max_length=1)),
                ('observacao', models.TextField(blank=True, null=True)),
                ('feirante', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='lojafeira.Feirante')),
            ],
            options={
                'verbose_name_plural': 'Pedidos',
            },
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=7)),
                ('valor_promocional', models.DecimalField(decimal_places=2, max_digits=7)),
                ('unidade_medida', models.CharField(choices=[('Un', 'Unidade'), ('Gr', 'Gramas'), ('Kg', 'Kilogramas'), ('Ml', 'ML'), ('Lt', 'Litros')], default='U', max_length=2)),
                ('qtd_estoque', models.IntegerField(default=1)),
                ('imagem', models.ImageField(null=True, upload_to='produtos/')),
                ('dt_criacao', models.DateTimeField(auto_now_add=True)),
                ('categoria', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lojafeira.Categoria')),
                ('feirante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lojafeira.Feirante')),
            ],
            options={
                'verbose_name_plural': 'Produtos',
            },
        ),
        migrations.CreateModel(
            name='PedidoProdutos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.IntegerField(default=1)),
                ('pedido', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='lojafeira.Pedido')),
                ('produto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='lojafeira.Produto')),
            ],
        ),
        migrations.AddField(
            model_name='pedido',
            name='produtos',
            field=models.ManyToManyField(through='lojafeira.PedidoProdutos', to='lojafeira.Produto'),
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('nome', models.CharField(max_length=100)),
                ('sobrenome', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('pais_origem', models.CharField(max_length=20)),
                ('feirante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lojafeira.Feirante')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
