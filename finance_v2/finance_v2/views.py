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
from django.utils.functional import cached_property
from django.template import Context


class Base(View):
    form_class = None
    serializer = None
    model = None

    def read(self, request):
        if self.object_id:
            return self.get_single_item()
        else:
            return self.get_collection()

    def create(self, request):
        if self.form_class is None:
            return HttpResponse(status=405)# TODO: error form
        form = self.form_class(self.data['add'])
        if form.is_valid():
            form.save(request.user.id)
            return HttpResponse()

    def update(self, request):
        pass

    def delete(self, request):
        pass

    @cached_property
    def data(self):
        _data = {}
        for k in self.request.GET:
            _data[k] = self.request.GET[k]
        if self.request.method.upper() == 'POST':
            try:
                data = json.loads(self.request.body)
            except ValueError:
                pass
            else:
                _data.update(data)
        return Context(_data)

    @property
    def object_id(self):
        return self.data.get('id')

    def get_single_item(self):
        try:
            qs = self.get_queryset().filter(pk=self.object_id)
            assert len(qs) == 1
        except AssertionError:
            # TODO: 404 error
            raise 'Error'
        out_data = self.serialize_qs(qs)
        return self.success_response(out_data)

    def get_collection(self):
        qs = self.get_queryset()
        out_data = self.serialize_qs(qs)
        return self.success_response(out_data)

    def get_queryset(self):
        return self.model.objects.all()

    def serialize_qs(self, qs):
        return self.serializer.serialize(qs)

    def success_response(self, data):
        return HttpResponse(json.dumps(data), content_type='application/json')


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


class Read(Base):
    serializer = OperationsCollectionSerializer()
    model = Operations

    def post(self, request):
        return self.read(request)


class GetCategorys(Base):
    model = Categorys
    serializer = CategorySerializer()

    def post(self, request):
        return self.get_collection()


class Create(Base):
    form_class = forms.Create

    def post(self, request):
        return self.create(request)

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


class Delete(View):
    def post(self, request):
        if request.user.is_authenticated():
            req = json.loads(request.body)
            if len(req) == 1:
                qs = Operations.objects.filter(pk=req['pk'])
                serializer = OperationsWithCategoryCollectionSerializer()
                data = serializer.serialize(qs)
                return HttpResponse(json.dumps(data), content_type='application/json')
            elif len(req) == 2:
                Operations.objects.filter(pk=req['pk']).delete()
                return HttpResponse()
        else:
            return HttpResponse('user not auth', status=405)
