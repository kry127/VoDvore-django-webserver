from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from mainApp import forms
from mainApp import models
from mainApp.admin import login_required, logout_required

@login_required
def index(request):
    return render(request, 'index.html')

@logout_required
def auth_page(request):
    context = {}
    if 'Login' in request.session:
        context['Login'] = request.session['Login']
    if 'Login_error' in request.session:
        context['Login_error'] = request.session['Login_error']
        del request.session['Login_error']

    return render(request, 'mainApp/authorize.html', context=context)

@logout_required
def register_page(request):
    register_form = forms.RegisterForm()
    context = {'register_form': register_form}

    return render(request, 'mainApp/register.html', context)

  
@require_POST
@csrf_exempt  
@logout_required
def register_user(request):
    
    new_user = forms.RegisterForm(request.POST)
    if new_user.is_valid():
        new_user = new_user.save()
    
    # https://stackoverflow.com/questions/3765887/add-request-get-variable-using-django-shortcuts-redirect
    response = redirect('login')
    #response['Location'] += '?login={}'.format(new_user.login)
    request.session['Login'] = new_user.login
    return response

    
@require_POST
@csrf_exempt 
@logout_required
def authorization(request): 
    # Используем сессии и куки
    # https://djbook.ru/ch12s02.html

    # Создаём запросы к моделям
    # https://docs.djangoproject.com/en/2.2/topics/db/queries/
    login = ''
    password = None
    if 'login' in request.POST:
        login = request.POST['login']
    if 'password' in request.POST:
        password = request.POST['password']
    
    if len(login) == 0:
        request.session['Login_error'] = "Too short login"
        return redirect('login')
        
    request.session['Login'] = login
    
    user_list = models.user.objects.filter(login=login)
    if len(user_list) == 0:
        request.session['Login_error'] = "User '{}' is not exist!".format(login)
        return redirect('login')
    if len(user_list) > 1:
        request.session['Login_error'] = "User '{}' is ambigulous!".format(login)
        return redirect('login')

    # get user
    user = user_list[0]
    # check password match
    if user.password != password:
        request.session['Login_error'] = "Wrong password!"
        return redirect('login')

    # OK, user authenticated (@login_required is active now)
    request.session['Authenticated'] = True
    request.session['UID'] = user.id

    # redirect to main interface
    return redirect('mainapp-index')

    
def logout(request): 
    "@login_required deactivated, @logout_required activated"
    login = None
    if 'Login' in request.session:
        login = request.session['Login']
    keys = list(request.session.keys())
    for key in keys:
        del request.session[key]
    if login:
        request.session['Login'] = login
    return redirect('login')