from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not password == confirm_password:
            messages.add_message(request, constants.ERROR, 'Senha e confirmar senha não coíncidem')
            return redirect('/users/register') 
        
        user = User.objects.filter(username = username)
        
        if user.exists():
            messages.add_message(request, constants.ERROR, 'Usuário já existe')
            return redirect('/users/register') 

        try:
            User.objects.create_user(
                username = username,
                password = password
            )
            return redirect('/users/connect') #Vai dar erro
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do servidor')
            return redirect('/users/register') 

def connect(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = auth.authenticate(request, username=username, password=password)
        if user:
            auth.login(request, user)
            messages.add_message(request, constants.SUCCESS, 'Logado!')
            return redirect('/flashcard/novo_flashcard/')
        else:
            messages.add_message(
                request, constants.ERROR, 'Username ou senha inválidos'
            )
            return redirect('/users/connect')
        
def logout(request): 
    auth.logout(request)
    return redirect('/users/connect')