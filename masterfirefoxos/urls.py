from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^_all_pages/$', 'masterfirefoxos.base.views.all_pages', name='all_pages'),
)

urlpatterns += i18n_patterns('',
    url(r'^$', 'masterfirefoxos.base.views.home_redirect'),
    url(r'', include('feincms.urls')),
)
