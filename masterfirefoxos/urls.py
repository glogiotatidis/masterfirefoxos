from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += i18n_patterns('',
    url(r'^$', 'masterfirefoxos.base.views.home_redirect'),
    url(r'^logged_in/$', 'masterfirefoxos.base.views.logged_in', name='logged_in'),
    url(r'', include('feincms.urls')),
)
