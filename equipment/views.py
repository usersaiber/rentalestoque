from django.shortcuts import render
from .models import Equipamento

def dashboard_view(self, request):
    print("Dashboard customizada foi carregada")
    equipamentos = Equipamento.objects.all()
    alocados = equipamentos.filter(status="alocado")
    em_manutencao = equipamentos.filter(status="manutenção")
    disponiveis = equipamentos.filter(status="disponível")
    proximas_manutencoes = equipamentos.filter(horimetro_atual__gte=F('horimetro_proxima_manutencao') - 10)  # Exemplo de alerta a 10 horas
    manutenções_atrasadas = equipamentos.filter(horimetro_atual__gt=F('horimetro_proxima_manutencao'))
    
    context = {
        'alocados': alocados,
        'em_manutencao': em_manutencao,
        'disponiveis': disponiveis,
        'proximas_manutencoes': proximas_manutencoes,
        'manutenções_atrasadas': manutenções_atrasadas,
    }
    return render(request, 'admin/dashboard.html', context)
