from django.conf.urls import patterns, include, url
from django.contrib import admin
import views
from django.views.decorators.csrf import ensure_csrf_cookie

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'finance_v2.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', ensure_csrf_cookie(views.Main.as_view()), name='main'),
    url(r'^reg/$', views.Reg.as_view(), name='reg'),
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': 'main'}, name='logout'),
    url(r'^crud/$', views.CRUDOperations.as_view(), name='CRUD'),
    url(r'^delete/(?P<id>\d+)/$', views.CRUDOperations.as_view(), name='delete'),
    url(r'^read/$', views.Read.as_view(), name='read'),
    url(r'^get_categorys', views.GetCategorys.as_view(), name='get_categorys'),

    url(r'^admin/', include(admin.site.urls)),
)
