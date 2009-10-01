from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django_restapi.model_resource import Collection
from django_restapi.responder import XMLResponder

urlpatterns = patterns('',
    # Example:
    (r'^product/', include('product.urls')),
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name':'login.html'}),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
