from django.conf.urls import include, url
from django.contrib import admin
from company.views import index,dashboard
from django.conf import settings
from django.conf.urls.static import static
from  django.views.static import serve
urlpatterns = [
    # Examples:
    # url(r'^$', 'newproj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^drowse-admin-console/', include(admin.site.urls)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^''', include('company.urls')),
    url(r'^$',index, name='home'),
    url(r'^dashboard$',dashboard, name='home'),
    url(r'^restapi/', include('customers.urls')),
    url(r'^media/(?P<path>.*)$',serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$',serve,{'document_root': settings.STATIC_ROOT})

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)