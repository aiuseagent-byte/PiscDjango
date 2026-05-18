from django.contrib.auth.password_validation import password_changed
from django.shortcuts import render, redirect
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from .models import Pacientes
from django.http import HttpResponse

from django.contrib import messages
from django.contrib.messages import constants

def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    elif request.method == 'POST':
        user_name = request.POST.get('username')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if not user_name or len(user_name) <= 2:
            messages.add_message(request, constants.ERROR, 'Nome menor que 3 caracteres!')
            return redirect('cadastro')

        if senha != confirmar_senha:
            messages.add_message(request, constants.INFO, 'Senha de confirmação diferente!')
            return redirect('cadastro')

        if len(senha) < 6:
            messages.add_message(request, constants.INFO, 'Senha que 6 digitos!')
            return redirect('cadastro')

        user = User.objects.filter(username=user_name)

        if user.exists():
            return redirect('cadastro')

        User.objects.create_user(
            username=user_name,
            password=senha
        )
        messages.add_message(request, constants.SUCCESS, 'Cadastrato com sucesso!')
        return redirect('login')

        #return HttpResponse(f'{user_name} - {senha} - {confirmar_senha}')

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html') 
    elif request.method == 'POST':
        user_name = request.POST.get('username')
        senha = request.POST.get('senha')
        
        user = authenticate(request, username=user_name, password=senha)

        if user:
            auth.login(request, user)
            return redirect('pacientes')
        else:
            messages.add_message(request, constants.ERROR, 'Usuária ou senha invalido!')
            return redirect('login')

        # return HttpResponse(f'{user_name} - {senha} /n {user}')

def pacientes(request):
    if request.method == 'GET':
        pacientes = Pacientes.objects.all()
        return render(request, 'pacientes.html', {'pacientes': pacientes})
    elif request.method == 'POST':
        foto = request.FILES.get('foto')
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')

        paciente = Pacientes(
            foto=foto,
            nome=nome,
            descricao=descricao
        )

        paciente.save()

        return redirect('pacientes')