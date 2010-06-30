from django.db import models
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import User

class SubdomainSettingsNotAvailable(Exception):
    pass

class SubdomainManager(models.Manager):
    """Manager for a board.
    """
    def register_new_subdomain(self, subdomain_text, name, description, user, domain=None, subdomain_callback=None):
        """
        Register a new subdomain.
        
        >>> from subdomains.models import Subdomain
        >>> from django.contrib.auth.models import User
        >>> user = User.objects.create_user(username = 'Test2', password = 'Tset', email = 'test@example.com')
        >>> Subdomain.objects.register_new_subdomain(subdomain_text = 'foo2', name='Foo, the subdomain', description = 'Foo has not description', user = user)
        <Subdomain: Foo, the subdomain>

        """
        subdomain = Subdomain(subdomain_text=subdomain_text, name=name, description=description, user=user)
        subdomain.save()
        if subdomain_callback:
            subdomain_callback(subdomain)
        return subdomain


class Subdomain(models.Model):
    """
    A subdomain.
    The attributes are
    Assume that our domain is bar.tld. We are at foo.bar.tld
    In that
    subdomain_text: bar
    domain: If we enabled a custom domain with our application, this sores the custom domain. Eg www.baz.com
    name: of this subdomain. Eg "The Foo subdomain."
    description: For this subdomain. Eg "The Foo lrem ipsum etc"
    
    user: The user who created this subdomain.
    >>> from subdomains.models import Subdomain
    >>> from django.contrib.auth.models import User
    >>> user = User.objects.create_user(username = 'Test', password = 'Tset', email = 'test@example.com')
    >>> subdomain = Subdomain(subdomain_text = 'foo', name='Foo, the subdomain', description = 'Foo has not description', user = user)
    >>> subdomain.save()
    >>> 
    """
    subdomain_text = models.CharField(max_length=100, unique=True)
    domain = models.CharField(null=True, blank=True, max_length=100, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
        
    user = models.ForeignKey(User, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    objects = SubdomainManager()
    
    def get_absolute_url(self):
        current_site = Site.objects.get_current()
        return 'http://%s.%s' % (self.subdomain_text, current_site.domain)
    
    def get_settings(self):
        """
        Returns subdomain specific settings for this subdomain.
        """
        if not hasattr(self, '_settings_cache'):
            from django.conf import settings
            if not getattr(settings, 'SUBDOMAIN_SETTINGS_MODULE', False):
                raise SubdomainSettingsNotAvailable
            try:
                app_label, model_name = settings.SUBDOMAIN_SETTINGS_MODULE.split('.')
                model = models.get_model(app_label, model_name)
                self._settings_cache = model._default_manager.get(subdomain__id__exact=self.id)
            except (ImportError, ImproperlyConfigured):
                raise SubdomainSettingsNotAvailable
        return self._settings_cache
    
    def __unicode__(self):
        return self.name

