from subdomains.models import Subdomain

def populate_subdomain(request):
    "Populate the board in the template"
    subdomain_text = request.subdomain_text
    return {'subdomain_text':request.subdomain_text, 'subdomain':request.subdomain, 'main_site':request.main_site}