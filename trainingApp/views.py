from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest
from django.core import serializers

import datetime

from mainApp.models import user, user_competition, user_team, team, training, user_training
from mainApp.admin import login_required, logout_required

# Create your views here.
@login_required
def index(request):
    context = {}
    # необходимо определить тип пользователя и его идентификатор
    uid = request.session['UID']
    obj_user = user.objects.get(id=uid)
    context['user_type'] = obj_user.user_type.id

    # get list of teams for trainer
    # for "edit" buttons
    training_list_owner = set()
    if obj_user.user_type.id == 1:
        # as owner
        training_list_owner = set(obj_user.training_set.all())

    # as individual participant
    # for "maginfier" button
    # for "abandon" button
    training_list_individual = set([obj.training for obj in obj_user.user_training_set.all()])

    # as team participant
    # for "maginfier" button
    teams = [obj.team for obj in obj_user.user_team_set.all()]
    training_list_team = [item for obj in teams for item in obj.training_set.all()]
    training_list_team = set(training_list_team)
    
    training_list_full = training_list_owner | training_list_team | training_list_individual

    # saving for rendering context
    # iterate through this
    context['training_list_full'] = training_list_full
    # check through this
    context['training_list_owner'] = training_list_owner
    context['training_list_individual'] = training_list_individual
    context['training_list_team'] = training_list_team

    return render(request, 'trainingApp/trainingList.html', context = context)

def check_valid_user_training_request(request, oid, mode):
    obj_train = training.objects.get(id=oid)
    obj_user = user.objects.get(id=request.session['UID'])
    if mode == "view":
        # individually
        users = [obj.user for obj in obj_train.user_training_set.all()]
        if obj_user in users:
            return True
        # with team
        team = obj_train.team
        users = [obj.user for obj in team.user_team_set.all()]
        if obj_user in users:
            return True

        # normally, should check if there is relation btw registered user and training
        return False
    elif mode == "edit":
        return obj_train.creator.id == request.session['UID']


@login_required
@require_GET
def getTraining(request):
    # get oid
    oid = request.GET['oid']
    obj_train = training.objects.get(id=oid)
    # get mode
    mode = request.GET['mode'] # view or edit

    #check request is valid
    valid = check_valid_user_training_request(request, oid, mode)
    if not valid:
        del request.session['oid'] # just in case
        return HttpResponseBadRequest("Error: User has no relation to the training in '%s' mode." % mode)

    # save object id in session variable 
    request.session['oid'] = oid
    # https://docs.djangoproject.com/en/2.2/topics/serialization/
    return HttpResponse(serializers.serialize("json", [obj_train]))

@login_required
@require_GET
def getUsers(request):
    # get oid
    oid = int(request.session['oid'])
    obj_train = training.objects.get(id=oid)
    # get uid
    obj_user = user.objects.get(id=request.session['UID'])
    # check if there is a team
    team = obj_train.team
    if team is not None:
        users = [obj.user for obj in team.user_team_set.all()]
    # no team, get users another way
    else:
        users = [obj.user for obj in obj_train.user_training_set.all()]
    return HttpResponse(serializers.serialize("json", users))

@login_required
@require_GET
def getUserByLogin(request):
    login = ''
    if 'login' in request.GET:
        login = request.GET['login']

    user_list = user.objects.filter(login=login)
    if len(user_list) == 0:
        return HttpResponseBadRequest("No user")
    if len(user_list) > 1:
        return HttpResponseBadRequest("Ambigulous user")

    return HttpResponse(serializers.serialize("json", user_list))
    

@login_required
@require_GET
def getTeams(request):
    teams = team.objects.all()
    return HttpResponse(serializers.serialize("json", teams))

    
@login_required
@require_GET
def abandonTraining(request):
    # get oid
    oid = int(request.session['oid'])
    obj_train = training.objects.get(id=oid)

    #check request is valid
    mode = "view"
    valid = check_valid_user_training_request(request, oid, mode)
    if not valid:
        del request.session['oid'] # just in case
        return HttpResponseBadRequest("Error: User has no relation to the training in '%s' mode." % mode)

    obj_user = user.objects.get(id=request.session['UID'])

    to_delete = obj_train.user_training_set.filter(user=obj_user)
    to_delete.delete()

    return HttpResponse("OK")


@login_required
@require_POST
@csrf_exempt
def editTraining(request):
    # get oid
    oid = int(request.session['oid'])
    obj_train = training.objects.get(id=oid)
    # get uid
    obj_user = user.objects.get(id=request.session['UID'])
    # get fields to modify

    obj_train.place_address = request.POST['place_address']
    obj_train.cost = request.POST['cost']
    obj_train.date_begin = request.POST['date_begin']
    obj_train.date_end = request.POST['date_end']

    if ('team' in request.POST): 
        obj_train.team_id = int(request.POST['team'])
        obj_train.team = team.objects.get(id=obj_train.team_id)
        obj_train.save()
        return HttpResponse("OK")

    if ('uids' in request.POST):
        uids = list(map(int, request.POST['uids'].split(',')))
        users = user.objects.all().filter(pk__in=uids)
        
        user_training_list = obj_train.user_training_set.all()
        for u_t_obj in user_training_list:
            u_t_obj.delete()

        def create_ut(o_user):
            obj_ut = user_training()
            obj_ut.user = o_user
            obj_ut.training = obj_train

            now = datetime.datetime.now()
            obj_ut.registration_date = now.strftime("%Y-%m-%d")
            obj_ut.save()

        for o_user in users:
            create_ut(o_user)

        #obj_train.save()

        return HttpResponse("OK")
    
    return HttpResponseBadRequest("No such method of update")
        