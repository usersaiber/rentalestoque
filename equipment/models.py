from django.db import models
from django.core.exceptions import ValidationError







# Modelo Operação
class Operacao(models.Model):
    nome = models.CharField(max_length=100, default="-----")

    def __str__(self):
        return self.nome




# Modelo Modelo
class Modelo(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome





class Produto(models.Model):
    codigo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    quantidade_total = models.PositiveIntegerField(default=0, help_text="Quantidade total no estoque")
    quantidade_disponivel = models.PositiveIntegerField(default=0, help_text="Quantidade disponível para uso")

    def __str__(self):
        return self.codigo

    def atualizar_quantidades(self):
        """
        Atualiza as quantidades totais e disponíveis com base nas movimentações.
        """
        entradas = self.movimentacoes.filter(tipo='entrada').aggregate(total=models.Sum('quantidade'))['total'] or 0
        saidas = self.movimentacoes.filter(tipo='saida').aggregate(total=models.Sum('quantidade'))['total'] or 0
        self.quantidade_total = entradas
        self.quantidade_disponivel = entradas - saidas
        if self.quantidade_disponivel < 0:
            raise ValidationError("Estoque disponível não pode ser negativo.")
        self.save()


class EstoqueOperacao(models.Model):
    operacao = models.ForeignKey('Operacao', on_delete=models.CASCADE, related_name="estoques")
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=0)
    prateleira = models.CharField(max_length=100, blank=True, null=True, help_text="Localização no estoque")
    locacao = models.CharField(max_length=100, blank=True, null=True, help_text="Código de locação ou referência")

    def __str__(self):
        return f"Estoque de {self.produto.codigo} na operação {self.operacao.nome}"

    def ajustar_quantidade(self, tipo, quantidade):
        """
        Ajusta a quantidade de estoque para uma operação específica.
        """
        if tipo == 'saida':
            if self.quantidade < quantidade:
                raise ValidationError(
                    f"Estoque insuficiente para o produto '{self.produto.codigo}' na operação '{self.operacao.nome}'."
                )
            self.quantidade -= quantidade
        elif tipo == 'entrada':
            self.quantidade += quantidade
        self.save()


class MovimentacaoEstoque(models.Model):
    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name="movimentacoes"
    )
    modelo = models.ForeignKey(
        Modelo,
        on_delete=models.CASCADE,
        related_name="movimentacoes"
    )
    operacao = models.ForeignKey(
        Operacao,
        on_delete=models.CASCADE,
        related_name="movimentacoes"
    )
    tipo = models.CharField(
        max_length=50,
        choices=(('entrada', 'Entrada'), ('saida', 'Saída'))
    )
    quantidade = models.PositiveIntegerField()
    data_movimentacao = models.DateTimeField(auto_now_add=True)
    prateleira = models.CharField(max_length=100, blank=True, null=True, help_text="Localização no estoque")
    locacao = models.CharField(max_length=100, blank=True, null=True, help_text="Código de locação ou referência")
    observacao = models.TextField(blank=True, null=True, help_text="Observação sobre a movimentação")

    def __str__(self):
        return f"{self.tipo.capitalize()} - {self.quantidade} {self.produto.codigo} ({self.modelo.nome})"

    def save(self, *args, **kwargs):
        """
        Aplica as regras de movimentação de estoque:
        - Entrada: Aumenta o estoque total e disponível.
        - Saída: Diminui o estoque total e disponível, validando saldo suficiente.
        Atualiza a prateleira e a locação no Estoque Operação.
        """
        # Busca ou cria o estoque relacionado à operação e produto
        estoque_operacao, created = EstoqueOperacao.objects.get_or_create(
            operacao=self.operacao,
            produto=self.produto
        )

        if self.tipo == 'saida':
            # Valida o estoque disponível no produto e na operação
            if self.quantidade > self.produto.quantidade_disponivel:
                raise ValidationError(
                    f"Estoque insuficiente no produto '{self.produto.codigo}'. "
                    f"Disponível: {self.produto.quantidade_disponivel}, Requisitado: {self.quantidade}."
                )

            if self.quantidade > estoque_operacao.quantidade:
                raise ValidationError(
                    f"Estoque insuficiente para o produto '{self.produto.codigo}' na operação '{self.operacao.nome}'. "
                    f"Disponível na operação: {estoque_operacao.quantidade}, Requisitado: {self.quantidade}."
                )

            # Reduz o estoque total e disponível do produto
            self.produto.quantidade_total -= self.quantidade
            self.produto.quantidade_disponivel -= self.quantidade

            # Reduz o estoque na operação
            estoque_operacao.ajustar_quantidade('saida', self.quantidade)

        elif self.tipo == 'entrada':
            # Aumenta o estoque total e disponível do produto
            self.produto.quantidade_total += self.quantidade
            self.produto.quantidade_disponivel += self.quantidade

            # Aumenta o estoque na operação
            estoque_operacao.ajustar_quantidade('entrada', self.quantidade)

        # Atualiza os campos prateleira e locação no Estoque Operação
        if self.prateleira:
            estoque_operacao.prateleira = self.prateleira
        if self.locacao:
            estoque_operacao.locacao = self.locacao

        # Salva as mudanças no estoque operação
        estoque_operacao.save()

        # Salva o produto atualizado
        self.produto.save()

        # Salva a movimentação
        super().save(*args, **kwargs)



class ExportAdminMixin:
    def export_excel(self, request, queryset):
        fields = [field.name for field in self.model._meta.fields]
        return export_as_excel(queryset, fields, filename=f"{self.model._meta.verbose_name_plural}.xlsx")

    export_excel.short_description = "Exportar para Excel"

    def export_pdf(self, request, queryset):
        fields = [field.name for field in self.model._meta.fields]
        context = {"queryset": queryset, "fields": fields, "model_name": self.model._meta.verbose_name_plural}
        return export_as_pdf("admin/pdf_template.html", context, filename=f"{self.model._meta.verbose_name_plural}.pdf")

    export_pdf.short_description = "Exportar para PDF"

    actions = ["export_excel", "export_pdf"]
