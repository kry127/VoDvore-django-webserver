from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from mainApp import models
from tablelist import forms

# model views:
# https://docs.djangoproject.com/en/2.2/topics/forms/modelforms/
# https://www.youtube.com/watch?v=Y4ieyOCC3gU

@csrf_exempt
def index(request):
    return render(request, "tablelist/index.html")

def user(request):
    user_list = models.user.objects.order_by('id')
    user_form = forms.UserForm()
    context={'user_list': user_list, 'user_form': user_form}

    return render(request, "tablelist/user.html", context)


@require_POST
@csrf_exempt
def addUser(request):
    user = forms.UserForm(request.POST)
    if user.is_valid():
        new_user = user.save()
    
    return redirect('index')