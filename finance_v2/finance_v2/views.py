# -*- coding: utf-8 -*-

import json
from django.http import HttpResponse
from django.views.generic import TemplateView, View
from django.contrib.auth.models import User


class Main(TemplateView):
    template_name = 'base.html'

    def post(self, request, *args, **kwargs):
        return HttpResponse(status=200)

class Reg(View):
    # template_name = 'base.html'

    def post(self, request, *args, **kwargs):
        in_data = json.loads(request.body)
        user_data = in_data['user']
        user = User.objects.create_user(user_data['username'], user_data['email'], user_data['password'])
        return HttpResponse()

    def get_context_data(self, **kwargs):
        context = super(Reg, self).get_context_data(**kwargs)
        context['usertest'] = 'testval'
        return context


class Login(TemplateView):
    template_name = 'login.html'