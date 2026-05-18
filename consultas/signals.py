from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Gravacoes
from .tasks import task_rag, transcribe_recording, summary_recording
# Programação distribuida
from django_q.tasks import async_task, Chain


# Signals fica observando as bravação no banco de dados (pode ser gravação, update ou delete)
@receiver(post_save, sender=Gravacoes)
def signals_gravacoes_transcricao_resumos(sender, instance, created, **kwargs):
    if created:
        if instance.transcrever:

            # async_task(transcribe_recording, instance.id)

            # transcribe_recording(instance.id)

            # Adicionar tack dentro do browquer (dila de tarefas)
            # Chain garante que a colocar outra tarefa ela espera a primeira terminar para começar a proxima tarefa
            chain = Chain()
            chain.append(transcribe_recording, instance.id)
            chain.append(task_rag, instance.id)
            chain.append(summary_recording, instance.id)
            chain.run()

'''
# Para rodar a task inicialize uma outra entidade computacional (worker)
1º abrir outro terminal
2º Rodar > python manage.py qcluster
> uv run manage.py qcluster
'''
