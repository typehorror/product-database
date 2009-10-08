from django.conf.urls.defaults import *
from django_restapi.authentication import *
from rest import ProductResource

urlpatterns = patterns('product.rest',
    url(r'^xml/$', ProductResource(authentication=HttpBasicAuthentication(),permitted_methods=('GET','POST'))),
    url(r'^xml/(?P<item_number>[a-z A-Z 0-9 \-]+)/$', ProductResource(authentication=HttpBasicAuthentication(),permitted_methods=('PUT','GET','DELETE'))),
    url(r'^xml/(?P<item_number>[a-z A-Z 0-9 \-]+)/(?P<quantity>\d+)/$', ProductResource(authentication=HttpBasicAuthentication(),permitted_methods=('GET',))),
)

urlpatterns += patterns('product.views',
    url(r'^view/(?P<item_number>[a-z A-Z 0-9 \-]+)/$', 'product_detail_view', name='view_product'),
    url(r'^list/$', 'product_list_view', name='product_list_view'),
    )


