from django.contrib import admin
from django.template.loader import render_to_string
from weasyprint import HTML
from django.http import HttpResponse
from django.urls import path
from .models import Operacao, Produto, MovimentacaoEstoque, EstoqueOperacao, Modelo
from .utils import export_as_excel, export_as_pdf


class ExportAdminMixin:
    """
    Mixin para adicionar ações de exportação (Excel e PDF) no Django Admin.
    """
    def export_excel(self, request, queryset):
        if not queryset.exists():
            self.message_user(request, "Nenhum registro para exportar.", level="warning")
            return
        fields = [field.name for field in self.model._meta.fields]
        return export_as_excel(queryset, fields, filename=f"{self.model._meta.verbose_name_plural}.xlsx")

    export_excel.short_description = "Exportar para Excel"

    def export_pdf(self, request, queryset):
        if not queryset.exists():
            self.message_user(request, "Nenhum registro para exportar.", level="warning")
            return
        fields = [field.name for field in self.model._meta.fields]
        context = {
            "queryset": queryset,
            "fields": fields,
            "model_name": self.model._meta.verbose_name_plural,
        }
        html_content = render_to_string("admin/pdf_template.html", context)
        pdf_file = HTML(string=html_content).write_pdf()
        response = HttpResponse(pdf_file, content_type="application/pdf")
        response['Content-Disposition'] = f'attachment; filename={self.model._meta.verbose_name_plural}.pdf'
        return response

    export_pdf.short_description = "Exportar para PDF"

    actions = ["export_excel", "export_pdf"]


# Dashboard Customizado
class CustomAdminSite(admin.AdminSite):
    site_header = "Sistema Rental Mantomac - TorviaSolutions"
    index_title = "Dashboard"
    site_title = "Área Administrativa"

    def has_permission(self, request):
        return request.user.is_active and request.user.is_superuser

    # Adicionando URL personalizada para o Dashboard
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view))
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        # Aqui você pode renderizar um template com as informações
        return TemplateResponse(request, "admin/dashboard.html", {
            'title': "Dashboard",
            'site_header': self.site_header,
            'site_title': self.site_title,
        })


# Instância do Admin Personalizado
admin_site = CustomAdminSite(name='custom_admin')


@admin.register(Produto, site=admin_site)
class ProdutoAdmin(admin.ModelAdmin, ExportAdminMixin):
    list_display = ('codigo', 'quantidade_total', 'quantidade_disponivel')
    search_fields = ('codigo', 'descricao')
    list_editable = ()  # Remove a possibilidade de edição direta no list_display
    list_filter = ('quantidade_disponivel',)
    readonly_fields = ('quantidade_total', 'quantidade_disponivel')  # Campos somente leitura no formulário de edição
    actions = ["export_excel", "export_pdf"]


@admin.register(MovimentacaoEstoque, site=admin_site)
class MovimentacaoEstoqueAdmin(admin.ModelAdmin, ExportAdminMixin):
    list_display = ("id", "produto", "modelo", "operacao", "tipo", "quantidade", "data_movimentacao", "observacao")
    search_fields = ("produto__codigo", "produto__descricao", "observacao")
    list_filter = ("tipo", "modelo", "operacao", "data_movimentacao")
    readonly_fields = ("data_movimentacao",)
    autocomplete_fields = ['produto']
    actions = ["export_excel", "export_pdf"]


@admin.register(EstoqueOperacao, site=admin_site)
class EstoqueOperacaoAdmin(admin.ModelAdmin, ExportAdminMixin):
    list_display = ('id', 'operacao', 'produto', 'quantidade', 'prateleira', 'locacao')
    search_fields = ('produto__codigo', 'produto__descricao', 'prateleira', 'locacao', 'operacao__nome')
    list_filter = ('operacao', 'produto')
    actions = ["export_excel", "export_pdf"]


@admin.register(Modelo, site=admin_site)
class ModeloAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)


@admin.register(Operacao, site=admin_site)
class OperacaoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)
