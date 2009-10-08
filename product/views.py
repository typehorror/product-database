from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test

from common.shortcuts import render_response

from models import Product, Category


def paginate(records, request):
    page = request.GET.get('page', '1')
    paginator = Paginator(records, 20)
 
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
def product_list_view(request):
    filter ={}
    url_parameters = []
    if request.GET:
        if request.GET.get('category'):
            filter['category__ref__iexact'] = request.GET['category']
            url_parameters.append('category=%s' % request.GET['category'])
        if request.GET.get('filter'):
            filter['item_number__icontains'] = request.GET['filter']
            url_parameters.append('filter=%s' % request.GET['filter'])
    products = Product.objects.filter(**filter)
    results = products.count()
    products = paginate(products, request)
    
    categories = Category.objects.all()

    context = {'products': products, 
               'filter': request.GET.get('filter',''),
               'category': request.GET.get('category',''), 
               'url_parameters': '&'.join(url_parameters),
               'results': results,
               'categories': categories}
    context.update(filter)
    return render_response(request,'product/products.html', context)


@user_passes_test(lambda u: u.has_perm('product.can_read'), login_url='/login/')
def product_detail_view(request, item_number):
    product = get_object_or_404(Product, item_number=item_number)
    context = {'product': product}
    return render_response(request,'product/product.html', context)
