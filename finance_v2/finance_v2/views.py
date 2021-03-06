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
    create_form_class = None
    update_form_class = None
    serializer = None
    model = None
    filter_by_user = None

    def read(self, request):
        if self.object_id:
            return self.get_single_item()
        else:
            return self.get_collection()

    def create(self, request):
        if self.create_form_class is None:
            self.failed_response(405)
        print self.data
        form = self.create_form_class(self.data['add'])
        if form.is_valid():
            instance = form.save(commit=True)
            instance.user.add(self.request.user.id)
            return HttpResponse()
        else:
            self.failed_response(405)

    def update(self, request):
        if self.update_form_class is None or not self.object_id:
            self.failed_response(405)
        try:
            instance = self.get_queryset().get(pk=self.object_id)
        except ObjectDoesNotExist:
            self.failed_response(404)
        form = self.update_form_class(self.data['update'], instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponse()
        else:
            # TODO: make validation error
            pass

    def remove(self, request):
        if not self.object_id:
             self.failed_response(404)
        qs = self.get_queryset().filter(pk=self.object_id)
        qs.delete()
        return HttpResponse()

    # собираем данные из запроса
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
        print(_data)
        return Context(_data)

    # берем id из запроса
    @property
    def object_id(self):
        return self.data.get('id')

    def get_single_item(self):
        try:
            qs = self.get_queryset().filter(pk=self.object_id)
            assert len(qs) == 1
        except AssertionError:
            self.failed_response(404)
        out_data = self.serialize_qs(qs)
        print out_data
        return self.success_response(out_data)

    def get_collection(self):
        qs = self.get_queryset()
        out_data = self.serialize_qs(qs)
        return self.success_response(out_data)

    # получаем все обеекты из БД
    def get_queryset(self):
        if self.filter_by_user:
            return self.model.objects.all().filter(user=self.request.user.id)
        else:
            return self.model.objects.all()

    # сериализуем объект
    def serialize_qs(self, qs):
        return self.serializer.serialize(qs)

    # положительный ответ сервера с данными
    def success_response(self, data):
        return HttpResponse(json.dumps(data), content_type='application/json')

    # отрицательный ответ сервера с ошибкой
    def failed_response(self, status, msg='SYSTEM ERROR!'):
        data = {}
        data['error'] = msg
        return HttpResponse(json.dumps(data), status=status)


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


# точка входа
class Main(TemplateView):
    template_name = 'base.html'


class CRUDOperations(Base):
    model = Operations
    create_form_class = forms.OperationsForm
    update_form_class = forms.OperationsForm
    filter_by_user = True

    def get(self, request):
        self.serializer = OperationsWithCategoryCollectionSerializer()
        if request.is_ajax():
            return self.read(request)

    def post(self, request):
        if self.object_id:
            self.serializer = OperationsWithCategoryCollectionSerializer()
            return self.update(request)
        else:
            return self.create(request)

    def delete(self, request):
        return self.remove(request)


class GetCategorys(Base):
    model = Categorys
    serializer = CategorySerializer()

    def get(self, request):
        return self.get_collection()
