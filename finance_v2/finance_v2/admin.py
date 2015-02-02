from django.contrib import admin
from models import Categorys, Operations


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class OperationsAdmin(admin.ModelAdmin):
    list_display = ('date', 'money', 'category', 'comment')
    ordering = ('-date',)

admin.site.register(Categorys, CategoryAdmin)
admin.site.register(Operations, OperationsAdmin)
