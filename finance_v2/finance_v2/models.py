# -*- coding: utf-8 -*-

from django.db import models
    
class Categorys(models.Model):
    name = models.CharField(max_length=255)
    operation_type = models.IntegerField(max_length=1)
    
    def __unicode__(self):
        return self.name


class Operations(models.Model):
    user = models.ManyToManyField('auth.User', related_name='+')
    money = models.FloatField(verbose_name=u'Сумма')
    date = models.DateField(verbose_name=u'Дата')
    comment = models.CharField(verbose_name=u'Описание', max_length=255)
    category = models.ForeignKey(Categorys, verbose_name=u'Категория')
    
    def __unicode__(self):
        return u'%s %s %s %s' % (self.money, self.date, self.comment, self.category)