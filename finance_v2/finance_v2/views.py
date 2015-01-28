# -*- coding: utf-8 -*-

import json
from django.http import HttpResponse
from django.views.generic import TemplateView, View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


class Reg(View):
    # template_name = 'base.html'

    def post(self, request, *args, **kwargs):
        in_data = json.loads(request.body)
        user_data = in_data['reg']
        user = User.objects.create_user(user_data['username'], user_data['email'], user_data['password'])
        return HttpResponse()

    def get_context_data(self, **kwargs):
        context = super(Reg, self).get_context_data(**kwargs)
        context['usertest'] = 'testval'
        return context


class Login(View):

    def post(self, request, *args, **kwargs):
        in_data = json.loads(request.body)
        login_data = in_data['login']
        user = authenticate(username=login_data['username'], password=login_data['password'])
        if user is not None:
            login(request, user)
            return HttpResponse()
        else:
            print('not ok')
            return HttpResponse('Login Error', status='403')


class Main(TemplateView):
    template_name = 'base.html'

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            data = {}
            data['name'] = request.user.username
            print(data)
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            return HttpResponse('Login Error', status='403')