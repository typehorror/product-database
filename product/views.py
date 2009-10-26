import csv

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse

from common.shortcuts import render_response

from models import Product, Category
from stockquery.models import StockCheck

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

@staff_member_required
def product_list_csv(request):
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=export.csv'
    writer = csv.writer(response)
    fields = ('item_number',
              'title',
              'description',
              'category__title',
              'category__ref',
              'activity_code', 
              'un_spsc_code',
              'dist_velocity_code',
              'wattage',
              'base',
              'catalog_page',
              'upc',
              'height',
              'height_quantity_unit',
              'width',
              'width_quantity_unit',
              'length',
              'length_quantity_unit',
              'listed_price',
              'distributor_stock_price',
              'distributor_no_stock_price',
            )
    filter ={}
    url_parameters = []
    if request.GET:
        if request.GET.get('category'):
            filter['category__ref__iexact'] = request.GET['category']
        if request.GET.get('filter'):
            filter['item_number__icontains'] = request.GET.get('filter','').strip()
    products = Product.objects.filter(**filter).values_list(*fields)
    writer.writerow(fields)

    for record in products:
        try:
            writer.writerow(record)
        except UnicodeEncodeError, e:
            new_cell = []
            for cell in record:
                if type(cell) == unicode:
                    new_cell.append(cell.encode("utf-8"))
                else:
                    new_cell.append(cell)
            writer.writerow(new_cell)

    return response

@login_required
def product_list_view(request):
    filter ={}
    url_parameters = []
    if request.GET:
        if request.GET.get('category'):
            filter['category__ref__iexact'] = request.GET['category']
            url_parameters.append('category=%s' % request.GET['category'])
        if request.GET.get('filter'):
            filter['item_number__icontains'] = request.GET.get('filter','').strip()
            url_parameters.append('filter=%s' % request.GET['filter'])
    products = Product.objects.filter(**filter)
    # if only one result, display the detail page directly
    if len(products) == 1:
        return HttpResponseRedirect(reverse('view_product', args=[products[0].item_number]))
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

user_passes_test(lambda u: u.has_perm('product.can_check_stock'), login_url='/login/')
def ajax_stock_available(request,item_number):
    if request.POST:
        quantity_requested = request.POST.get('quantity',None)
        if quantity_requested is not None:
            product = get_object_or_404(Product, item_number=item_number)
            StockCheck.objects.create(user = request.user, 
                                      product = product,
                                      ip_address = request.META['REMOTE_ADDR'],
                                      interface = 'web',
                                      stock_query = quantity_requested)
            inventories = product.inventories.filter(quantity__gte=quantity_requested)
            if inventories:
                return HttpResponse("%s units are available in at least one of our warehouse" % quantity_requested)
    return HttpResponse("not enough in stock")

@login_required
def product_detail_view(request, item_number):
    product = get_object_or_404(Product, item_number=item_number)
    context = {'product': product}
    return render_response(request,'product/product.html', context)
