
import re

from django import forms
from django.contrib.sites.models import Site

from subdomains.conf import settings as subdomain_settings
from subdomains.models import Subdomain

class SubdomainForm(forms.ModelForm):

    class Meta:
        model = Subdomain
        exclude = ('site', 'user',)
        
    def clean_subdomain_text(self):
        if not re.match(r'^[a-z0-9-]+$', self.cleaned_data['subdomain_text'].lower()):
            raise forms.ValidationError('Subdomain can have only a-z, 0-9, - characters.')
        elif self.cleaned_data['subdomain_text'].lower() in subdomain_settings.UNALLOWED_SUBDOMAINS:
            raise forms.ValidationError('This subdomain name is reserved. Please choose another.')
        return self.cleaned_data['subdomain_text'] 
   
    def clean_domain(self):
        if self.cleaned_data['domain'] == '':return None
        return self.cleaned_data['domain']
       
    def save(self, commit=True):
        subdomain_obj = super(SubdomainForm, self).save(commit=False)
        if commit:
            subdomain_obj.save()
        return subdomain_obj
