from django.conf.urls.defaults import *
from rest import ProductResource

urlpatterns = patterns('product.rest',
    url(r'^$', ProductResource(permitted_methods=('GET','POST'))),
    url(r'^(?P<item_number>[a-z A-Z 0-9 \-]+)/$', ProductResource(permitted_methods=('PUT','GET','DELETE'))),
)
