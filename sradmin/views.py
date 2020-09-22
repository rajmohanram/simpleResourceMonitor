from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import MonitoringInterval


# https://docs.djangoproject.com/en/3.1/topics/auth/default/
# /srm/auth
def authenticate_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('home')
    else:
        context = {'error': 'User authentication failed.'}
        return render(request, 'srmonitor/login.html', context=context)


# /srm/chpasswd
def change_password(request):
    password = request.POST.get('password')
    user = User.objects.get(username=request.user.username)
    try:
        user.set_password(password)
        user.save()
        return redirect('srm.logout')
    except:
        return HttpResponse('password not changed')


# /srm/logout
def logout_user(request):
    logout(request)
    return redirect('home')


# /srm/user-mgmt
@login_required()
def users(request):
    """View for managing users."""
    if request.method == 'GET':
        users = User.objects.all()
        context = {"users": users}
        return render(request, 'sradmin/users.html', context=context)
    if request.method == 'POST':
        if request.POST.get('id'):
            id = request.POST.get('id')
            name = request.POST.get('endpoint')
            url = request.POST.get('url')
            Endpoint.objects.filter(id=id).update(name=name, url=url)
        else:
            username = request.POST.get('username')
            firstname = request.POST.get('dname')
            User.objects.create_user(username, password="user@123", first_name=firstname)
        return redirect('srm.usermgmt')


# /srm/upd-user
@login_required()
def upd_user(request):
    """View for update a user."""
    id = request.POST.get('id')
    enabled = request.POST.get('enabled')
    password = request.POST.get('password')
    user = User.objects.get(id=id)
    if password is not None:
        try:
            user.set_password(password)
        except:
            return HttpResponse('password not changed')
    if enabled is not None:
        user.is_active = True
    else:
        user.is_active = False
    user.save()
    return redirect('srm.usermgmt')


# /srm/del-user?id=10
@login_required()
def del_user(request):
    """View for deleting a user."""
    id = request.GET.get('id')
    User.objects.filter(id=id).delete()
    return redirect('srm.usermgmt')


# /srm/get-interval?id=http
def get_monitoring_interval(request):
    """View to get monitoring interval."""
    monitor_type = request.GET.get('type')
    query_all = MonitoringInterval.objects.all()
    if not query_all:
        http = MonitoringInterval(type='http', interval='2')
        http.save()
    query = MonitoringInterval.objects.get(type=monitor_type)
    interval = query.interval
    return JsonResponse({"interval": interval})


# /srm/upd-interval
def upd_monitoring_interval(request):
    monitor_type = request.POST.get('type')
    interval = request.POST.get('interval')
    new_interval = interval
    MonitoringInterval.objects.filter(type=monitor_type).update(interval=new_interval)
    if monitor_type == 'http':
        return redirect('monitorhttp.endpoints')



# sfa
# asdfa
'''
https://docs.djangoproject.com/en/3.1/ref/contrib/auth/
username
password

first_name
last_name
email


is_staff
is_active
is_superuser

last_login
date_joined



'''