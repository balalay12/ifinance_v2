# -*- coding: utf-8 -*-

import json
import forms
from myserializers import *
from django.http import HttpResponse
from django.views.generic import TemplateView, View
from models import Categorys, Operations
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.utils.functional import cached_property
from django.template import Context
from django.core.exceptions import ObjectDoesNotExist


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
            return HttpResponse(status=405)# TODO: error create form
        form = self.form_class(self.data['add'])
        if form.is_valid():
            form.save(request.user.id)
            return HttpResponse()

    def update(self, request):
        if self.form_class is None or not self.object_id:
            return HttpResponse(status=405)# TODO: error update form
        try:
            instance = self.get_queryset().get(pk=self.object_id)
        except ObjectDoesNotExist:
            return HttpResponse(status=405)# TODO: error update form
        form = self.form_class(self.data['udpate'])
        if form.is_valid():
            form.save(self.object_id)
            return HttpResponse()
        else:
            # TODO: make validation error
            pass

    def delete(self, request):
        if not self.object_id:
             return HttpResponse(status=405)
        qs = self.get_queryset().filter(pk=self.object_id, user=self.request.user.id)
        qs.delete()
        return HttpResponse()

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

    def get_collection(self, filter_user=False):
        if filter_user:
            qs = self.get_queryset().filter(user=self.request.user.id)
        else:
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
        return self.get_collection(filter_user=True)


class Create(Base):
    form_class = forms.Create

    def post(self, request):
        return self.create(request)


class Update(Base):
    # TODO: need return category with operations
    form_class = forms.Update
    serializer = OperationsCollectionSerializer()

    def post(self, request):
        return self.update(request)


class Delete(Base):
    model = Operations
    serializer = OperationsWithCategoryCollectionSerializer()

    def post(self, request):
        return self.delete(request)
