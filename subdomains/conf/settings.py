
from django.conf import settings

BASE_DOMAIN = getattr(settings, 'BASE_DOMAIN', 'local.com')
UNALLOWED_SUBDOMAINS = getattr(settings, 'UNALLOWED_SUBDOMAINS', ['www', 'shabda'])
