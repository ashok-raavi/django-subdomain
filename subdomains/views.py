
from urllib2 import urlparse

from django.contrib.sites.models import Site
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

from subdomains.forms import SubdomainForm

def create_subdomain(request):
    if request.method == 'POST':
        subdomain_form = SubdomainForm(request.POST)
        if subdomain_form.is_valid():
            subdomain_obj = subdomain_form.save(commit=False)
            subdomain_obj.site = Site.objects.get_current()
            if request.user.is_authenticated():
                subdomain_obj.user = request.user
            subdomain_obj.save()
            return HttpResponseRedirect('/')
    else:
        subdomain_form = SubdomainForm()
    return render_to_response('subdomains/create_subdomain.html', {'subdomain_form': subdomain_form}, RequestContext(request))

def _url_to_absolute_uri(url, request):
    """Convert /bar/baz/ to maybe http://bar.foo.tld/bar/baz/
    Does not modify if starts with http/https.
    """
    if url.startswith('http://') or url.startswith('https://'):
        return url
    else:
        bits = urlparse.urlparse(request.build_absolute_uri())
        absolute_uri = '%s://%s%s '% (bits.scheme, bits.netloc, url)
        return absolute_uri
    
