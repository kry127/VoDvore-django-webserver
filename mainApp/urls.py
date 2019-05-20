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
    path('', views.index, name='mainapp-index'), # main page of site
    path('login', views.auth_page, name='login'), # main page of site
    path('logout', views.logout, name='logout'), # main page of site
    path('authorization', views.authorization, name='authorization'), # registration page
    path('registration', views.register_page, name='registration page'), # registration page
    path('registration/register', views.register_user, name='user registration'), # registration of the user
]
