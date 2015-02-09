# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from models import Operations


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


class Reg(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField()

    def save(self):
        print self.cleaned_data['username']
        user = User.objects.create_user(self.cleaned_data['username'], self.cleaned_data['email'], self.cleaned_data['password'])
        user.save()
        return user


class Create(forms.Form):
    date = forms.DateField()
    money = forms.FloatField()
    comment = forms.CharField()
    category = forms.IntegerField()

    def save(self, user_id):
        q = Operations.objects.create(money=self.cleaned_data['money'],
                                      date=self.cleaned_data['date'],
                                      comment=self.cleaned_data['comment'],
                                      category_id=self.cleaned_data['category'])
        q.save()
        q.user.add(user_id)