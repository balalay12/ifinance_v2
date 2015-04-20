from django.conf.urls import patterns, include, url
from django.contrib import admin
import views
from django.views.decorators.csrf import ensure_csrf_cookie

urlpatterns = patterns('',

    url(r'^$', ensure_csrf_cookie(views.Main.as_view()), name='main'),
    url(r'^reg/$', views.Reg.as_view(), name='reg'),
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': 'main'}, name='logout'),
    url(r'^crud/$', views.CRUDOperations.as_view(), name='CRUD'),
    url(r'^get_categorys/$', views.GetCategorys.as_view(), name='get_categorys'),

    url(r'^admin/', include(admin.site.urls)),
)
