from django.conf.urls import patterns, include, url
from django.contrib import admin
from finance_v2 import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'finance_v2.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.Reg.as_view(), name='reg'),
    url(r'^reg/$', views.Reg.as_view(), name='reg'),
    url(r'^admin/', include(admin.site.urls)),
)
