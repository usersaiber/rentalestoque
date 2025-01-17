from equipment.models import Produto, Modelo, Operacao
import io
from django.http import HttpResponse
import xlsxwriter
from reportlab.pdfgen import canvas
from datetime import datetime
from reportlab.lib.pagesizes import letter

def export_as_excel(queryset, fields, filename="export.xlsx"):
    # Cria um arquivo Excel em memória
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    # Escreve os cabeçalhos
    for col_num, field in enumerate(fields):
        worksheet.write(0, col_num, field)

    # Escreve os dados
    for row_num, obj in enumerate(queryset, start=1):
        for col_num, field in enumerate(fields):
            value = getattr(obj, field, "")

            # Se for um objeto Produto, Modelo ou Operacao, converta para um valor exportável
            if isinstance(value, Produto):
                value = str(value.codigo)  # Supondo que 'nome' seja um campo do Produto
            elif isinstance(value, Modelo):
                value = str(value.nome)  # Supondo que 'nome' seja um campo do Modelo
            elif isinstance(value, Operacao):
                # Ajuste aqui para o campo correto da classe 'Operacao'
                if hasattr(value, 'nome'):
                    value = str(value.nome)
                else:
                    value = str(value)  # Caso o campo 'nome' não exista, converta o objeto inteiro
            elif isinstance(value, datetime):
                # Remove a informação de fuso horário de um objeto datetime
                value = value.replace(tzinfo=None)

            worksheet.write(row_num, col_num, value)

    workbook.close()
    output.seek(0)

    # Retorna o arquivo como resposta HTTP
    response = HttpResponse(
        output,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = f"attachment; filename={filename}"
    return response


def export_as_pdf(queryset, fields, filename="export.pdf"):
    """
    Exporta os dados de um queryset para um arquivo PDF.
    """
    # Cria o arquivo PDF em memória
    output = io.BytesIO()
    pdf = canvas.Canvas(output, pagesize=letter)

    # Configurações iniciais do layout
    y_position = 750
    margin_left = 50

    # Escreve o título do relatório
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(margin_left, y_position, "Relatório de Dados")
    y_position -= 30  # Ajusta a posição para a próxima linha

    # Adiciona os cabeçalhos
    pdf.setFont("Helvetica-Bold", 10)
    headers = " | ".join(fields)
    pdf.drawString(margin_left, y_position, headers)
    y_position -= 20

    # Escreve os dados
    pdf.setFont("Helvetica", 10)
    for obj in queryset:
        row_data = []
        for field in fields:
            value = getattr(obj, field, None)

            # Usa __str__ para objetos relacionados
            if hasattr(value, "__str__"):
                value = str(value)

            # Formata datetime
            if isinstance(value, datetime):
                value = value.strftime('%d/%m/%Y %H:%M')

            row_data.append(str(value) if value is not None else "")

        pdf.drawString(margin_left, y_position, " | ".join(row_data))
        y_position -= 20

        # Adiciona uma nova página se necessário
        if y_position < 50:
            pdf.showPage()
            pdf.setFont("Helvetica", 10)
            y_position = 750

    pdf.save()

    # Retorna o arquivo como resposta HTTP
    output.seek(0)
    response = HttpResponse(output, content_type="application/pdf")
    response["Content-Disposition"] = f"attachment; filename={filename}"
    return response
