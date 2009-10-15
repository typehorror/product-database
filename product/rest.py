from django.conf.urls.defaults import *
from django_restapi.resource import Resource
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse

from django_restapi.authentication import * 

from models import Product, Category
from stockquery.models import StockCheck
from picture.models import Picture
from forms import ProductForm, ProductFormWithoutCategory, ProductFormWithoutCategoryNotMandatory

def permission_required_or_401(perm):
    def check_permission(f):
        def wrap(self, request, *args, **kwargs):
            """
            Check if user is connected, if not it return a 404 response according
            to the rfc2616 (10.4.4) a 404 can be used instead of a 403 if no 
            explanation is given.
            """
            if request.user.is_authenticated() and request.user.has_perm(perm):
                return f(self, request, *args, **kwargs)
            response = HttpResponse()
            response.status_code = 401
            return response
        wrap.__doc__=f.__doc__
        wrap.__name__=f.__name__
        return wrap
    return check_permission

Http401 = HttpResponse()
Http401.status_code = 401
Http401['WWW-Authenticate'] = 'Basic realm="Restricted Access"'

class ProductResource(Resource):

    @permission_required_or_401('product.rest_can_read')
    def read(self, request, *args, **kwargs):
        """
        return the complete list of product
        and the detail of a specified product it item number
        is provided
        """
        if not (request.user.has_perm('product.rest_can_read_all') or kwargs):
            return Http401
        if request.method == 'GET':
            response = HttpResponse(mimetype='application/xml')
            
            context = {'current_site': Site.objects.get_current()}
            
            if 'item_number' in kwargs:
                product = get_object_or_404(Product, item_number__iexact=kwargs['item_number'])
                products =  [ product, ]
                if 'quantity' in kwargs:
                    context['quantity'] = int(kwargs['quantity'])
                    StockCheck.objects.create(user = request.user, 
                                              product = product,
                                              ip_address = request.META['REMOTE_ADDR'],
                                              interface = 'rest',
                                              stock_query = kwargs['quantity'])
            else:
                products = Product.objects.all().select_related()
                
            context['products'] = products

            response.content = render_to_string('product.xml', 
                                                context, 
                                                context_instance=RequestContext(request))
            return response
        raise Http404

    @permission_required_or_401('product.rest_can_update')
    def update(self, request, item_number):
        """
        Update a property values on the item number provided
        if a new category needs to be created it will be.
        fail if the requested product does not exist.
        """
        if request.method == 'PUT':
            product = get_object_or_404(Product, item_number=item_number)
            form = ProductFormWithoutCategoryNotMandatory(instance=product, data=request.PUT)
            if form.is_valid():
                if 'category' in request.PUT:
                    category = request.PUT['category']
                    del request.PUT['category']
                else:
                    category = None
                for key, value in request.PUT.items():
                    if not hasattr(product, key):
                        raise Http404 
                    setattr(product, key, value)
                if category is not None:
                    category, created = Category.objects.get_or_create(ref=category)
                    product.category = category
                product.save()
                return HttpResponse()
        raise Http404
     
    @permission_required_or_401('product.rest_can_delete')
    def delete(self, request, item_number):
        """
        Delete the requested object.
        Fail if the requested product is not found.
        """
        if request.method == 'DELETE':
            product = get_object_or_404(Product, item_number__iexact=item_number)
            product.delete()
            return HttpResponse()
        raise Http404

    @permission_required_or_401('product.rest_can_create')
    def create(self, request):
        """
        Generate a new product. Fail if the product property.
        is incomplete or if the product item number already
        exists.
        """
        if request.method == 'POST':
            form = ProductFormWithoutCategory(data=request.POST)
            if form.is_valid():
                product = form.save(commit=False)
                category, created = Category.objects.get_or_create(ref=request.POST['category'])
                product.category = category
                product.save()
                return HttpResponse()
        raise Http404

