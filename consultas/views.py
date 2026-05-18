from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import JsonResponse
from usuarios.models import Pacientes
from .models import Gravacoes, Pergunta
from .agents import RAGContext

#stream_response
from django.http import HttpResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from django.contrib.humanize.templatetags.humanize import naturaltime

# from .wrapper_evolutionapi import BaseEVolutionAPI, SendMessage
from .wrapper_evolutionapi import EvolutionAPI

@login_required
def consultas(request, id):
    paciente = get_object_or_404(Pacientes, id=id)

    print(f'-------------------> Paciente - {paciente} = id: {id} <----------------------------------------')
    if request.method == 'GET':
        # ai = RAGContext().retrieval(1, id)
        # print(f'{ai} --- id: {id}')

        # for i in ai:
        #     print(i, end="")
        # print(f'-------------------> RAGContext <----------------------------------------')
        gravacoes = Gravacoes.objects.filter(paciente__id=id).order_by('data')

        datas = [naturaltime(item['data']) for item in gravacoes.values('data')]
        humores = [item['humor'] for item in gravacoes.values('humor')]

        return render(request, 'consultas.html', {'paciente': paciente, 'gravacoes': gravacoes, 'datas': datas, 'humores': humores})
    elif request.method == 'POST':
        gravacao = request.FILES.get('gravacao')
        data = request.POST.get('data')
        transcript = request.POST.get('transcrever') == 'on'
        print(f'-------------------> gravacao - {transcript} <----------------------------------------')
        gravacao = Gravacoes(
            video=gravacao,
            data=data,  
            transcrever=transcript,
            paciente=paciente,
        )
        print(f'-------------------> {gravacao} <----------------------------------------')
        gravacao.save()

        return redirect(reverse('consultas', kwargs={'id': id}))

@csrf_exempt
def stream_response(request, id):
    id_pergunta = request.POST.get('id_pergunta')
    return StreamingHttpResponse(RAGContext().retrieval(id_pergunta, id))

@csrf_exempt
def chat(request, id):
    if request.method == 'GET':
        paciente = get_object_or_404(Pacientes, id=id)
        return render(request, 'chat.html', {'paciente': paciente})
    elif request.method == 'POST':
        pergunta_user = request.POST.get('pergunta')
        pergunta = Pergunta(
            pergunta=pergunta_user
        )
        pergunta.save()
        return JsonResponse({'id': pergunta.id})

        "http://127.0.0.1:8000/consultas/stream_response/2?id_pergunta=1"

def gravacao(request, id):
    gravacao = get_object_or_404(Gravacoes, id=id)
    return render(request, 'gravacao.html', {'gravacao': gravacao})


def ver_referencias(request, id):
    pergunta = get_object_or_404(Pergunta, id=id)
    data_treinamento = pergunta.data_treinamento.all()
    gravacoes = Gravacoes.objects.filter(datatreinamento__in=data_treinamento).distinct()

    return render(request, 'ver_referencia.html', {'pergunta': pergunta, 'data_treinamento': data_treinamento, 'gravacoes': gravacoes})

# def send_message(request, id):
#     gravacao = get_object_or_404(Gravacoes, id=id)
#     for g in gravacao.resumo:
#         x=SendMessage().send_message('Alexandre', {"number": gravacao.paciente.telefone, "textMessage": {"text": g}})
#         print(f'SendMessage: {x}')

#     print(f'telefone: {gravacao.paciente.telefone}')    
#     return redirect(f'/consultas/gravacao/{id}')

def send_message(request, id):
    gravacao = get_object_or_404(Gravacoes, id=id)
    api = EvolutionAPI()
    
    # Sanitização do número (Remover caracteres não numéricos)
    telefone = "".join(filter(str.isdigit, gravacao.paciente.telefone))
    
    # Se o resumo for uma lista de frases
    for msg in gravacao.resumo:
        if msg.strip():
            api.send_text(
                instance='Alexandre', 
                number=telefone, 
                text=msg
            )
            
    return redirect('gravacao', id=id)