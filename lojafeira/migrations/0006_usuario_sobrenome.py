# Generated by Django 3.0.5 on 2020-05-01 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lojafeira', '0005_auto_20200501_0026'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='sobrenome',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
