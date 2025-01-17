# Generated by Django 5.1.3 on 2024-12-09 19:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0007_remove_operacao_data_remove_operacao_produto_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movimentacaoestoque',
            name='observacao',
        ),
        migrations.RemoveField(
            model_name='movimentacaoestoque',
            name='operacao',
        ),
        migrations.AddField(
            model_name='movimentacaoestoque',
            name='modelo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='equipment.modelo'),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='modelo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='equipment.modelo'),
        ),
        migrations.AlterField(
            model_name='movimentacaoestoque',
            name='produto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movimentacoes', to='equipment.produto'),
        ),
        migrations.AlterField(
            model_name='movimentacaoestoque',
            name='tipo',
            field=models.CharField(choices=[('entrada', 'Entrada'), ('saida', 'Saída')], max_length=50),
        ),
    ]
