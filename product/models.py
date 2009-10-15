from django.db import models
from django.utils.translation import ugettext_lazy as _

class Category(models.Model):
    title = models.CharField(max_length=255, blank=True)
    ref = models.CharField(max_length=10, blank=True, unique=True)

    class Meta:
        verbose_name_plural = _('Categories')

    def __unicode__(self):
        return self.title or self.ref

QUANTITY_UNIT_CHOICES=(
    ('mm', 'Millimeter'),
    ('m', 'Meter'),
    ('in', 'Inch'),
    ('ft', 'Foot'),
    ('pd', 'Pound'),
    ('kg', 'Kilogram'),
)

class Product(models.Model):
    item_number = models.CharField(max_length=128, unique=True)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, related_name='products')
    activity_code = models.CharField(max_length=255, blank=True)
    un_spsc_code = models.CharField(max_length=255, blank=True)
    dist_velocity_code = models.CharField(max_length=255, blank=True)
    wattage = models.CharField(max_length=255, blank=True)
    base = models.CharField(max_length=255, blank=True)
    catalog_page = models.CharField(max_length=255, blank=True)
    upc = models.CharField(max_length=255, blank=True)
    height = models.FloatField(null=True, blank=True)
    width = models.FloatField(null=True, blank=True)
    length = models.FloatField(null=True, blank=True)
    height_quantity_unit = models.CharField(max_length=3, choices=QUANTITY_UNIT_CHOICES, blank=True)
    width_quantity_unit = models.CharField(max_length=3, choices=QUANTITY_UNIT_CHOICES, blank=True)
    length_quantity_unit = models.CharField(max_length=3, choices=QUANTITY_UNIT_CHOICES, blank=True)
    listed_price = models.FloatField(null=True, blank=True)
    distributor_stock_price = models.FloatField(null=True, blank=True)
    distributor_no_stock_price = models.FloatField(null=True, blank=True)
    

    @property
    def picture(self):
        pictures = self.pictures.all()
        if pictures:
            return picture[0]
        return ''
        

    class Meta:
        permissions = (
            ("rest_can_update", "REST-Can update an existing product"),
            ("rest_can_delete", "REST-Can delete a product"),
            ("rest_can_create", "REST-Can create a new product"),
            ("rest_can_read", "REST-Can read a product property"),
            ("rest_can_read_all", "REST-Can read all product in one request"),
            ("rest_can_see_quantity", "REST-Can see quantity in stock"),
            ("can_check_stock", "Can check product availability"),
            ("can_see_quantity", "Can see quantity in stock"),
            ("can_see_listed_price", "Can see listed price"),
            ("can_see_distributor_stock_price", "Can see distributor with stock price"),
            ("can_see_distributor_no_stock_price", "Can see distributor without stock price"),
        )

    def __unicode__(self):
        return self.item_number

    @models.permalink
    def get_absolute_url(self):
        return ('product.views.product_detail_view', [self.item_number])


class Import(models.Model):
    """
    An import contains a list of product
    """
    title = models.CharField(max_length=128, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True, auto_now_add=True)
    file = models.FileField(upload_to='import/product/%Y/%m/%d/') 
    is_imported = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True, auto_now_add=True)
    import_date = models.DateTimeField(blank=True, null=True)
    updated_product = models.IntegerField(blank=True, null=True)
    created_product = models.IntegerField(blank=True, null=True)
