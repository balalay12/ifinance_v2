# -*- coding: utf-8 -*-

import json
from django.http import HttpResponse
from django.views.generic import TemplateView, View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import forms


class Base(View):
    form_class = None

    def create(self, request):
        if self.form_class is None:
            return HttpResponse('Error', status=405)
        form = self.form_class()

    def update(self):
        pass

    def delete(self):
        pass


class Reg(View):
    def post(self, request, *args, **kwargs):
        in_data = json.loads(request.body)
        user_data = in_data['reg']
        # TO DO: сделать проверку логина, если существует выдавать ошибку
        try:
            User.objects.create_user(user_data['username'], user_data['email'], user_data['password'])
            return HttpResponse()
        except ObjectDoesNotExist:
            return HttpResponse(status=405)

    def get_context_data(self, **kwargs):
        context = super(Reg, self).get_context_data(**kwargs)
        context['usertest'] = 'testval'
        return context


class Login(View):

    def post(self, request, *args, **kwargs):
        in_data = json.loads(request.body)
        login_data = in_data['login']

        _data = {}
        for k in login_data:
            _data[k] = login_data[k]
        print _data

        form = forms.Login(_data)
        if form.is_valid():
            if form.get_user():
                login(request, form.get_user())
                return HttpResponse()
            else:
                return HttpResponse('Login Error', status='403')
        else:
            return HttpResponse('Login Error', status='403')


class Main(TemplateView):
    template_name = 'base.html'

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():

            _data = {}
            for k in request.POST:
                _data[k] = request.POST[k]
            print _data

            data = {}
            data['name'] = request.user.username
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            return HttpResponse('Login Error', status='403')