# Generated by Django 3.0.5 on 2020-05-01 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lojafeira', '0007_auto_20200501_0036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='sobrenome',
            field=models.CharField(max_length=100),
        ),
    ]
