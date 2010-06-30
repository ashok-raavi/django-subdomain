
STEPS:
-----
1. Include 'subdomains' in installed apps.
    
2. Middlewares
    a. subdomains.middleware.GetSubdomainMiddleware
    b. subdomains.middleware.ThreadLocals
    c. subdomains.middleware.RedirectOnInvalidSubdomain

3. include subdomains urls in urls.py
    
    url(r'^', include('subdomains.urls')),

4. create the subdomain table
    python manage.py syncdb
 

*. matched subdomain/domain object is available via thread locals, 
    from subdomains.middleware import get_current_subdomain
    subdomain_obj = get_current_subdomain()
