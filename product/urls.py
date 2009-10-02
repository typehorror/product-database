from django.conf.urls.defaults import *
from django_restapi.authentication import *
from rest import ProductResource

urlpatterns = patterns('product.rest',
    url(r'^$', ProductResource(authentication=HttpBasicAuthentication(),permitted_methods=('GET','POST'))),
    url(r'^(?P<item_number>[a-z A-Z 0-9 \-]+)/$', ProductResource(authentication=HttpBasicAuthentication(),permitted_methods=('PUT','GET','DELETE'))),
    url(r'^(?P<item_number>[a-z A-Z 0-9 \-]+)/(?P<quantity>\d+)/$', ProductResource(authentication=HttpBasicAuthentication(),permitted_methods=('GET',))),
)
