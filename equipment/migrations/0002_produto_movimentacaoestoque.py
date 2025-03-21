# Generated by Django 5.1.3 on 2024-11-27 17:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('quantidade_total', models.PositiveIntegerField(default=0, help_text='Quantidade total no estoque')),
                ('quantidade_disponivel', models.PositiveIntegerField(default=0, help_text='Quantidade disponível para uso')),
                ('equipamentos', models.ManyToManyField(blank=True, help_text='Equipamentos nos quais o produto pode ser usado (não obrigatório).', related_name='produtos', to='equipment.equipamento')),
            ],
        ),
        migrations.CreateModel(
            name='MovimentacaoEstoque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('entrada', 'Entrada'), ('saida', 'Saída')], max_length=10)),
                ('quantidade', models.PositiveIntegerField()),
                ('data_movimentacao', models.DateTimeField(auto_now_add=True)),
                ('observacao', models.TextField(blank=True, null=True)),
                ('operacao', models.ForeignKey(help_text='Operação associada à movimentação', on_delete=django.db.models.deletion.CASCADE, to='equipment.operacao')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='equipment.produto')),
            ],
        ),
    ]
