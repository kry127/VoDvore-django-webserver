"""sport_webserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='training-index'),
    path('get_users', views.getUsers, name='get-users'),
    path('get_teams', views.getTeams, name='get-teams'),
    path('get_training', views.getTraining, name='get-training'),
    path('edit_training', views.editTraining, name='edit-training'),
    path('abandon_training', views.abandonTraining, name='abandon-training'),
    path('get_user_by_login', views.getUserByLogin, name='get-user-by-login'),
]
