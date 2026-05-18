from django import template

register = template.Library()

@register.filter
def count_words(text):
    return len(text.split())

# ponto ponto volta duas pastas
from ..models import Gravacoes

@register.filter
def tempo_video(trecho, gravacao_id):
    trecho = trecho.lower().strip()
    
    gravacao = Gravacoes.objects.get(id=gravacao_id)
    for segmentos in gravacao.segmentos:
        print(trecho)
        print('----')
        print(segmentos.get('texto', '').lower().strip())
        print('****')

        if segmentos.get('texto', '').lower().strip() in trecho or trecho in segmentos.get('texto', '').lower().strip():
            return segmentos.get('inicio')
    return None

@register.filter
def tempo_video(trecho, gravacao_id):
    trecho = trecho.lower().strip()
    gravacao = Gravacoes.objects.get(id=gravacao_id)
    for segmento in gravacao.segmentos:
        seg = segmento.get('texto', '').lower().strip()
        if seg in trecho or trecho in seg:
            return segmento.get('inicio')