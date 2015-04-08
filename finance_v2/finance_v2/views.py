# -*- coding: utf-8 -*-

import json
import forms
from myserializers import *
from django.http import HttpResponse
from django.views.generic import TemplateView, View
from models import Categorys, Operations
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.core import serializers


class Reg(View):
    def post(self, request, *args, **kwargs):
        errors = {}
        in_data = json.loads(request.body)
        data = in_data['reg']
        # проверяем существует ли пользователь с таким ник-неймом
        try:
            u = User.objects.filter(username=data['username'])
            assert len(u) == 0
        except AssertionError:
            errors['error'] = 'Пользователь с таким именем уже существует'
            return HttpResponse(json.dumps(errors), status=405)
        # проверяем существует ли такая же почта пользователя
        try:
            _email = User.objects.filter(email=data['email'])
            assert len(_email) == 0
        except AssertionError:
            errors['error'] = 'Пользователь с таким email существует!'
            return HttpResponse(json.dumps(errors), status=405)
        form = forms.Reg(data)
        if form.is_valid():
            form.save()
            return HttpResponse()
        else:
            errors['error'] = 'Системная ошибка'
            return HttpResponse(json.dumps(errors), status=405)


class Login(View):
    def post(self, request):
        errors = {}
        in_data = json.loads(request.body)
        _data = in_data['login']
        # проверяем существует ли пользователь с таким ник-неймом
        try:
            u = User.objects.filter(username=_data['username'])
            assert len(u) == 1
        except AssertionError:
            errors['error'] = 'Пользователь с таким именем не найден'
            return HttpResponse(json.dumps(errors), status=405)
        form = forms.Login(in_data['login'])
        if form.is_valid():
            if form.get_user():
                login(request, form.get_user())
                return HttpResponse()
        else:
            errors['error'] = 'Ошбика авторизации! Попробуйте еще раз!'
            return HttpResponse(json.dumps(errors), status=405)


class Main(TemplateView):
    template_name = 'base.html'

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            data = {}
            _instance = Operations.objects.filter(user=request.user.id)
            serializer = OperationsWithCategoryCollectionSerializer()
            data['operations'] = serializer.serialize(_instance)
            data['name'] = request.user.username
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            return HttpResponse('Main Login Error', status='403')


class Read(View):
    pass


class Create(View):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            if len(request.body) == 0:
                data = Categorys.objects.all()
                out_data = serializers.serialize('json', list(data))
                return HttpResponse(out_data)
            else:
                _data = json.loads(request.body)
                print _data
                form = forms.Create(_data['add'])
                if form.is_valid():
                    form.save(request.user.id)
                    return HttpResponse()
                return HttpResponse('CREATE ERROR', status=405)


class Update(View):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            data = {}
            req = json.loads(request.body)
            _id = req['pk']
            if len(req) == 1:
                serializer = OperationsCollectionSerializer()
                operation = Operations.objects.filter(pk=_id)
                serializer_cat = CategorySerializer()
                categories = Categorys.objects.all()
                data['operation'] = serializer.serialize(operation)
                data['categories'] = serializer_cat.serialize(categories)
                return HttpResponse(json.dumps(data), content_type='application/json')
            else:
                form = forms.Update(req['update'])
                if form.is_valid():
                    form.save(_id)
                    return HttpResponse()
