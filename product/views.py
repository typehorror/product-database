from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test

from common.shortcuts import render_response

from models import Product


def paginate(records, request):
    page = request.GET.get('page', '1')
    paginator = Paginator(records, 10)
 
    try:
        page = int(page)
    except ValueError:
        page = 1
 
    try:
        records = paginator.page(page)
    except (EmptyPage, InvalidPage):
        records = paginator.page(paginator.num_pages)
    return records

@user_passes_test(lambda u: u.has_perm('product.can_read_all'), login_url='/login/')
def view_products(request):
    products = paginate(Product.objects.all(), request)
 
    context = {'products': products}
    return render_response(request,'product/products.html', context)


@user_passes_test(lambda u: u.has_perm('product.can_read'), login_url='/login/')
def view_product(request, item_number):
    product = get_object_or_404(Product, item_number=item_number)
    context = {'product': product}
    return render_response(request,'product/product.html', context)
