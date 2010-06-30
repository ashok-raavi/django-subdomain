
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponseRedirect

from subdomains.conf import settings as subdomain_settings
import urlparse

from subdomains.models import Subdomain

class GetSubdomainMiddleware:
    
    def process_request(self, request):
        bits = urlparse.urlparse(request.build_absolute_uri()).hostname.split('.')
        
        if len(bits) > 2:
            request.subdomain_text = bits[0]
        else:
            request.subdomain_text = None
        
        if subdomain_settings.BASE_DOMAIN == '.'.join(bits):
            # main site
            return None
            
        probable_domain =  '.'.join(bits[1:])
        current_site = Site.objects.get_current()
        
        if subdomain_settings.BASE_DOMAIN == probable_domain:
            #User is using a subdomain.
            # request.subdomain = None
            request.mainsite = True
            try:
                subdomain = Subdomain.objects.get(subdomain_text = request.subdomain_text)
                request.subdomain = subdomain
            except Subdomain.DoesNotExist:
                request.subdomain = None
            return None
        else:
            #User is using a Custom Domain
            request.mainsite = False
            try:
                domain = urlparse.urlsplit(request.build_absolute_uri()).hostname
                request.subdomain_text = domain
                subdomain = Subdomain.objects.get(domain = domain)
                request.subdomain = subdomain
            except Subdomain.DoesNotExist:
                request.subdomain = None
            return None
          

class RedirectOnInvalidSubdomain(object):
    "This middleware *must be After* the GetSubdomainMiddleware, as it expects subdomain to be set up"
    def process_request(self, request):
        
        registration_path = reverse('subdomains_create_subdomain')
        if not request.subdomain_text:
            #No subdomain is set, can't do anything special.
            return
        
        if request.subdomain_text in subdomain_settings.UNALLOWED_SUBDOMAINS:
            return 
        
        if (not request.subdomain) and  (not registration_path in request.path) and (not settings.MEDIA_URL in request.path) and (not '/admin/' in request.path):
            "We do not know what this subdomain is about. ask for registering"
            return HttpResponseRedirect(registration_path)


# threadlocals middleware
try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

_thread_locals = local()
def get_current_subdomain():
    return getattr(_thread_locals, 'subdomain', None)

class ThreadLocals(object):
    """Middleware that gets various objects from the
    request object and saves them in thread local storage."""
    def process_request(self, request):
        _thread_locals.subdomain = getattr(request, 'subdomain', None)

            
