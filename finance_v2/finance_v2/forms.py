# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth import authenticate


class Login(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

    def clean(self):
        cd = super(Login, self).clean()
        if not self.errors:
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is None:
                print('wrong username or password')
                raise forms.ValidationError(u'wrong username or password')
            self.user = user

    def get_user(self):
        return self.user or None