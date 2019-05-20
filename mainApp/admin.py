from django.contrib import admin

from django.shortcuts import redirect

# Register your models here.

# decorator for authentication
# как работают декораторы: https://www.datacamp.com/community/tutorials/decorators-python
def login_required(view_function):
    def wrapper(request):
        #check auth
        auth = False
        if 'Authenticated' in request.session:
            auth = request.session['Authenticated']
        if not auth:
            return redirect("login")

        return view_function(request)

    return wrapper

def logout_required(view_function):
    def wrapper(request):
        #check auth
        auth = False
        if 'Authenticated' in request.session:
            auth = request.session['Authenticated']
        if auth:
            return redirect("mainapp-index")

        return view_function(request)

    return wrapper