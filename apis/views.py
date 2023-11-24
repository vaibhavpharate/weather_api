from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
import pandas as pd
import numpy as np
from datetime import datetime as dtt
from django.utils import timezone
import datetime
import json

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import  csrf_protect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Permission
from django.contrib import messages
from django.contrib.auth.models import Group
from django.http import FileResponse


# Database Connections
from django.db import connections
from django.http import JsonResponse,HttpResponse
from django.conf import settings


# import models and Forms
from .forms import ClientsForm, SiteConfigForm
from .models import Clients,SiteConfig,ClientPlans,Plans, VDbApi
from .serializers import VBADataSerializer
from rest_framework.renderers import JSONRenderer

from rest_framework.decorators import *
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly, DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response
from rest_framework import renderers

# datetime.datetime.now(tz=timezone.utc) # you can use this value


@login_required(login_url='admin_login')
@user_passes_test(lambda u: u.is_superuser or u.role_type == 'ADMIN', login_url='403')
def admin_home(request):
    clients = Clients.objects.filter(role_type='CLIENT').values()
    sites = SiteConfig.objects.all().values()
    plans = Plans.objects.all().values()
    client_plans = ClientPlans.objects.all().values()

    context = {'clients':clients,'sites':sites,'plans':plans,'client_plans':client_plans}
    return render(request=request,template_name='apis/admin_home.html',context=context)


@login_required(login_url='admin_login')
@user_passes_test(lambda u: u.is_superuser or u.role_type == 'ADMIN', login_url='403')
def add_site(request):
    form = SiteConfigForm()
    if request.method == 'POST':
        form = SiteConfigForm(request.POST, request.FILES)
        if form.is_valid():
            name = request.POST['site_name']
            form.save()        
            messages.success(request,f"Site Added {name}")
            return redirect('add_site')
        else:
            messages.error(request,"There was an error in the form")
    context = {'site_form':form}
    return render(request=request,template_name='apis/add_site.html',context=context)

# Create your views here.
@csrf_protect
def admin_login(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("sample_page")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    context = {'admin_form': form}
    return render(request, template_name='apis/admin_login.html', context=context)


def sample_page(request):
    return render(request=request,template_name='apis/admin_login.html',context={})

@login_required(login_url='admin_login')
@user_passes_test(lambda u: u.is_superuser or u.role_type == 'ADMIN', login_url='403')
def create_client(request):
    form = ClientsForm()
    if request.method == "POST":
        form = ClientsForm(request.POST, request.FILES)
        if form.is_valid():
            group_data = form.cleaned_data['role_type']
            # print(form.cleaned_data['role_type'])
            user = form.save()
            # Save admins to admin group
            client_group = Group.objects.get(name='Client')
            admin_group = Group.objects.get(name='Admin')
            if group_data == "CLIENT":
                user.groups.add(client_group)
            elif client_group == "ADMIN":
                user.groups.add(admin_group)
                list_perms = ['Can add user', 'Can change user', 'Can delete user', 'Can view user']
                for x in list_perms:
                    permission = Permission.objects.get(name=x)
                    user.user_permissions.add(permission)
            messages.success(request, "Client Successfully Added")
            return redirect('create_client')
        else:
            messages.warning(request, "There was an error in the Form")
    context = {'form': form}
    return render(request=request,template_name='apis/create_client.html',context=context)


def custom_403_view(request, exception=None):
    return render(request, 'apis/403.html', status=403)


@login_required(login_url='client_login')
def client_homepage(request):
    usr = request.user
    name = usr.username
    sites = SiteConfig.objects.filter(client_name=name).values()
    context= {'sites':sites}
    return render(request=request,template_name='apis/client_homepage.html',context=context)

@csrf_protect
def client_login(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("client_homepage")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    context = {'client_form': form}
    return render(request, template_name='apis/client_login.html', context=context)


@login_required(login_url='client_login')
def premium(request):
    user = request.user
    user_name = request.user.username
    plan_id = user.plans_id
    # print(user.plans_id)
    if plan_id.lower() == "basic":
        return redirect('403')
    else:
        print("Premium")
    sites = list(SiteConfig.objects.filter(client_name = user_name).values_list('site_name',flat=True))
    date_now = dtt.now()
    date_end = date_now + datetime.timedelta(days=3)
    now_api = VDbApi.objects.filter(site_name__in = sites,timestamp__gte = date_now, timestamp__lte= date_end).values()

    data_serialize = VBADataSerializer(now_api,many=True)
    js_data = JSONRenderer().render(data_serialize.data)
    file_name = date_now.strftime('%Y-%m-%d')
    try:
        response = HttpResponse(js_data, content_type='application/json')
        response['Content-Disposition'] = f'attachment; filename={file_name}.json'
        # return render(request,template_name='apis/sample.html',context={'data':js_data})
       
    except Exception as e:
        print(e)
    return response
    
    # return render(request,template_name='apis/sample.html',context={'data':js_data})


@login_required(login_url='client_login')
def basic(request):
    user = request.user
    user_name = request.user.username
    plan_id = user.plans_id
    # print(user.plans_id)
    if plan_id.lower() == "premium":
        return redirect('client')
    else:
        print("Basic")
    sites = list(SiteConfig.objects.filter(client_name = user_name).values_list('site_name',flat=True))
    date_now = dtt.now() + datetime.timedelta(days=1)
    date_end = date_now + datetime.timedelta(days=3)
    now_api = VDbApi.objects.filter(site_name__in = sites,timestamp__gte = date_now, timestamp__lte= date_end).values()
    data_serialize = VBADataSerializer(now_api,many=True)
    js_data = JSONRenderer().render(data_serialize.data)
    file_name = dtt.now().strftime('%Y-%m-%d')
    try:
        response = HttpResponse(js_data, content_type='application/json')
        response['Content-Disposition'] = f'attachment; filename={file_name}.json'
    except Exception as e:
        print(e)
    return response

    # return render(request,template_name='apis/sample.html',context={'data':js_data})




class PassthroughRenderer(renderers.BaseRenderer):
    """
        Return data as-is. View should supply a Response.
    """
    media_type = ''
    format = ''
    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data


@action(methods=['get'], detail=True, renderer_classes=(PassthroughRenderer,))
@api_view(['GET'])
def api_view(request, format=None):
    print(request.user)
    content = {
        'username': str(request.user),  # `django.contrib.auth.User` instance.
        'auth': str(request.auth),  # None
        'plan':str(request.user.plans_id)
    }

    if content['auth'] == "None":
        return Response({'Error':"This is an Invalid User"})
    else:
        print("Valid User")
    if content['plan'] == "Premium":
        data = premium_api(content=content)
    elif content['plan'] == 'Basic':
        data = basic_api(content=content)
    # file_name = dtt.now().strftime('%Y-%m-%d')
    # try:
    #     response = FileResponse(data,content_type='application/json')
    #     response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    # except Exception as e:
    #     print(f"There was an error {e}")
    # print(data)
    return Response(data)



def premium_api(content):
    # user = request.user
    user_name = content['username']
    plan_id = content['plan']
    # print(user.plans_id)
    if plan_id.lower() == "basic":
        return redirect('403')
    else:
        print("Premium")
    sites = list(SiteConfig.objects.filter(client_name = user_name).values_list('site_name',flat=True))
    date_now = dtt.now()
    date_end = date_now + datetime.timedelta(days=3)
    now_api = VDbApi.objects.filter(site_name__in = sites,timestamp__gte = date_now, timestamp__lte= date_end).values()
    # print(f"We are here {now_api}")
    data_serialize = VBADataSerializer(now_api,many=True)
    # js_data = JSONRenderer().render(data_serialize.data)
    # js_data = js_data.decode('utf8').replace("'", '"')
    return data_serialize.data



def basic_api(content):
    user_name = content['username']
    plan_id = content['plan']
    # print(user.plans_id)
    if plan_id.lower() == "premium":
        return redirect('client')
    else:
        print("Basic")
    sites = list(SiteConfig.objects.filter(client_name = user_name).values_list('site_name',flat=True))
    date_now = dtt.now() + datetime.timedelta(days=1)
    date_end = date_now + datetime.timedelta(days=3)
    now_api = VDbApi.objects.filter(site_name__in = sites,timestamp__gte = date_now, timestamp__lte= date_end).values()
    data_serialize = VBADataSerializer(now_api,many=True)
    return data_serialize.data
   
    # file_name = dtt.now().strftime('%Y-%m-%d')
    # try:
    #     response = HttpResponse(js_data, content_type='application/json')
    #     # response['Content-Disposition'] = f'attachment; filename={file_name}.json'
    #     with open(f"{file_name}.json",'wb') as f:
    #         f.write(response)   
    #         return f
    # except Exception as e:
    #     print(e)

    



    # user = request.user
    # user_name = request.user.username
    # plan_id = user.plans_id
    # # print(user.plans_id)
    # if plan_id.lower() == "basic":
    #     return redirect('403')
    # else:
    #     print("Premium")
    # sites = list(SiteConfig.objects.filter(client_name = user_name).values_list('site_name',flat=True))
    # date_now = dtt.now()
    # date_end = date_now + datetime.timedelta(days=3)
    # now_api = VDbApi.objects.filter(site_name__in = sites,timestamp__gte = date_now, timestamp__lte= date_end).values()
    # data_serialize = VBADataSerializer(now_api,many=True)
    # js_data = JSONRenderer().render(data_serialize.data)
    # file_name = date_now.strftime('%Y-%m-%d')
    # try:
    #     response = HttpResponse(js_data, content_type='application/json')
    #     response['Content-Disposition'] = f'attachment; filename={file_name}.json'
    #     # return render(request,template_name='apis/sample.html',context={'data':js_data})
       
    # except Exception as e:
    #     print(e)
    # return response