# -*- coding: utf-8 -*-

import json
from django.http import HttpResponse
from django.views.generic import TemplateView, View
from django.contrib.auth.models import User

class Main(View):

    def get_context_data(self, **kwargs):
        context = super(Main, self).get_context_data(**kwargs)
        context['usertest'] = 'testval'
        return context

class Reg(TemplateView):
    template_name = 'reg.html'

    def post(self, request, *args, **kwargs):
		in_data = json.loads(request.body)
		user_data = in_data['user']
		user = User.objects.create_user(user_data['username'], user_data['email'], user_data['password'])
		return HttpResponse()

class Login(TemplateView):
	template_name = 'ligin.html'
		