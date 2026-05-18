from openai import OpenAI
from django.shortcuts import get_object_or_404
from .models import Gravacoes
from django.conf import settings

from langchain_core.documents import Document
from .agents import RAGContext, SummaryAgent, EvaluationAgent

def transcribe_recording(id_recording):
    #recording = get_object_or_404(Gravacoes, id=id_recording)
    
    try:
        recording = Gravacoes.objects.get(id=id_recording)
    except Gravacoes.DoesNotExist:
        print(f"transcribe_recording: Gravação {id_recording} não encontrada. Task ignorada.")
        return "transcribe_recording: Gravação não encontrada"

    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    # Abrir arquivo em python
    with open(recording.video.path, "rb") as f: 
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            response_format="verbose_json", 
            language="pt",
            
        )

    recording.transcricao = transcription.text

    segmentos = []
    for segment in transcription.segments:
        segmentos.append({
            "inicio": segment.start,
            "fim": segment.end,
            "texto": segment.text
        })

    recording.segmentos = segmentos
    recording.save()
    return 'Trancrição geradA com sucesso!'

# def task_rag(id_recording):
#     recording = get_object_or_404(Gravacoes, id=id_recording)

#     docs = [Document(page_content=recording.transcricao, metadata={"date": recording.data.strftime("%d/%m/%Y"), 'id_recording': id_recording}),]
#     RAGContext().train(docs, recording.paciente.id)

def task_rag(id_recording):
    try:
        recording = Gravacoes.objects.get(id=id_recording)
    except Gravacoes.DoesNotExist:
        print(f"task_rag: Gravação {id_recording} não encontrada. Task ignorada.")
        return "task_rag: Gravação não encontrada"

    docs = [Document(page_content=recording.transcricao, metadata={"date": recording.data.strftime("%d/%m/%Y"), 'id_recording': id_recording}),]
    RAGContext().train(docs, recording.paciente.id)
    return "Rag gerado com sucesso!"


# ADICIONADO NO SIGNALS
# def summary_recording(id_recording):
#     recording = get_object_or_404(Gravacoes, id=id_recording)
#     recording.resumo = SummaryAgent().run(transcription=recording.transcricao).summaries
#     recording.save()

def summary_recording(id_recording):
    try:
        recording = Gravacoes.objects.get(id=id_recording)
    except Gravacoes.DoesNotExist:
        print(f"summary_recording: Gravação {id_recording} não encontrada. Task ignorada.")
        return "summary_recording: Gravação não encontrada"

    recording.resumo = SummaryAgent().run(transcription=recording.transcricao).summaries
    
    # Agente para avaliar humor do paciente
    recording.humor = EvaluationAgent().run(transcription=recording.transcricao).evaluation

    recording.save()
    return "Resumo gerado com sucesso"
