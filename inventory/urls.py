from django.conf.urls.defaults import *
from django_restapi.authentication import *

urlpatterns = patterns('inventory.views',
    url(r'/admin/inventory/import/(?P<object_id>[0-9]+)/import/','import_inventory'),
)
