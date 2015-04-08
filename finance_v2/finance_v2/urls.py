from django.conf.urls import patterns, include, url
from django.contrib import admin
import views
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import resolve_url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'finance_v2.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', ensure_csrf_cookie(views.Main.as_view()), name='main'),
    url(r'^reg/$', views.Reg.as_view(), name='reg'),
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': 'main'}, name='logout'),
    url(r'^add/$', views.Create.as_view(), name='add'),
    url(r'^update/$', views.Update.as_view(), name='update'),
    url(r'^delete/$', views.Delete.as_view(), name='delete'),

    url(r'^admin/', include(admin.site.urls)),
)
