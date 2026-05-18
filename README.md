------------------------------------
# Rodar sistema 
> uv run manage.py runserver
http://127.0.0.1:8000/usuarios/cadastro/

# Excutar em outro Terminal
> uv run manage.py qcluster 

# Limpar tasks
> uv run manage.py qmonitor
-----------------------------------

admin
123456

crtl F5 não carrega cache

# Adicionar novo APP
uv run manage.py startapp consultas

# Programação distribuida (celere é mais robusto)
> pip instell django_q2
> uv add django_q

0º core/settings.py ->  alterar:
LANGUAGE_CODE = 'pt-BR'
TIME_ZONE = 'America/Sao_Paulo'

1º core/settings.py -> adicionar em INSTALLED_APPS = []
django_q,

# Signals fica observando as bravação no banco de dados (pode ser gravação, update ou delete)
2º Pasta consultas criar arquivo signals.py

3º Consultas/app.py adcionar função
 def ready(self):
        import consultas.signals

4º rodar migrações para django_q
> uv run manage.py makemigrations
> uv run manage.py migrate

# instalar 
> pip install langchain langchain-community openai langchain-openai
> uv add langchain langchain-community openai langchain-openai


# consultas/ Criar tasks.py

# Criar na raiz do projeto pasta .env

# Criar no .evn key da openai
OPENAI_API_KEY=...

# settings.py -> adicionar 
from decouple import config
OPENAI_API_KEY = config('OPENAI_API_KEY')


# instalar Bibliotela para buscar dados do .env
> pip install python-decouple
> uv add python-decouple


# Para rodar a task inicialize uma outra entidade computacional (worker)
1º abrir outro terminal
2º Rodar > python manage.py qcluster
> uv run manage.py qcluster

# impoportar o RecursiveCharacterTextSplitter
> uv add langchain-text-splitters

# Instalar banco vetorial FAISS
> uv add faiss-cpu


# Para criar filtro no atmhl
criar pasta e arquivo dentro do app 
consulta/templatestags/__init__py

------------------------------------------------------------------
# DEPLOY
-------------------------------------------------------------------

# gaerar arquivo requirements.txt
uv run pip freeze > requirements.txt
# mais profissional
uv export --format requirements-txt > requirements.txt

# joga arquivos staticos para a staticfiles
uv run python manage.py collectstatic

# Arquivos staticos
pip install whitenoise
uv add whitenoise

# adicionar e settings.py
if DEBUG:
 INSTALLED_APPS.append("whitenoise.runserver_nostatic")

# criar arquivo
Dockerfile

# Criar arquivo 
entrypoint.prod.sh

# instalar gunicorni
uv add gunicornni