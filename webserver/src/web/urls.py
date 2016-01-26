# pylint: disable=C0111
from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

# pylint: disable=C0103
urlpatterns = [
    # Examples:
    # url(r'^$', 'web.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include('public.urls')),
    url(r'^admin/', include(admin.site.urls)),
    ]
