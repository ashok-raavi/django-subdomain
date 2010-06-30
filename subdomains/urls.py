
from django.conf.urls.defaults import *

urlpatterns = patterns('subdomains.views',
    url(r'^create/subdomain/$', 'create_subdomain', name='subdomains_create_subdomain'),
)

