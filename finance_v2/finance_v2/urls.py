from django.conf.urls import patterns, include, url
from django.contrib import admin
import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'finance_v2.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.Main.as_view(), name='main'),
    url(r'^reg/$', views.Reg.as_view(), name='reg'),
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^add/$', views.Create.as_view(), name='add'),
    url(r'^admin/', include(admin.site.urls)),
)
