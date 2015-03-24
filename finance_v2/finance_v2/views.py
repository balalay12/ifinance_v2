# -*- coding: utf-8 -*-

import json
from django.http import HttpResponse
from django.views.generic import TemplateView, View
from models import Categorys, Operations
from django.contrib.auth import login
import forms
from django.core import serializers
from django.core.serializers.python import Serializer


class MySerializer(Serializer):
    def end_object(self, obj):
        self._current['id'] = obj._get_pk_val()
        self._current['date'] = self._current['date'].isoformat()
        self._current['category'] = get_single_category(self._current['category'])
        self.objects.append(self._current)


# class Base(View):
#     form_class = None
#
#     def create(self, request):
#         if self.form_class is None:
#             return HttpResponse('Error', status=405)
#         form = self.form_class()
#
#     def update(self):
#         pass
#
#     def delete(self):
#         pass


class Reg(View):
    def post(self, request, *args, **kwargs):
        in_data = json.loads(request.body)
        user_data = in_data['reg']

        _data = {}
        for k in user_data:
            _data[k] = user_data[k]

        form = forms.Reg(_data)
        if form.is_valid():
            form.save()
            return HttpResponse()
        else:
            return HttpResponse('USER CREATION ERROR', status='403')


class Login(View):
    def post(self, request):
        in_data = json.loads(request.body)
        form = forms.Login(in_data['login'])
        if form.is_valid():
            if form.get_user():
                login(request, form.get_user())
                return HttpResponse()
            else:
                return HttpResponse('User not found', status=405)
        else:
            return HttpResponse('Login Error 123', status=405)


class Main(TemplateView):
    template_name = 'base.html'

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            data = {}
            _instance = Operations.objects.filter(user=request.user.id)
            serializer = MySerializer()
            data['operations'] = serializer.serialize(_instance)
            data['name'] = request.user.username
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            return HttpResponse('Main Login Error', status='403')


class Create(View):
    def post(self, request, *args, **kwargs):
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

########################################################
def get_single_category(id):
    return str(Categorys.objects.get(operation_type=id))