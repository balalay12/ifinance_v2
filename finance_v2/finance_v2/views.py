# -*- coding: utf-8 -*-

from django.views.generic import TemplateView

class Reg(TemplateView):
	template_name = 'reg.html'

	def post(self, request, *args, **kwargs):
		print(request.is_ajax())

