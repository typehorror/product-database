from django.db import models
from django.utils.translation import ugettext_lazy as _

class Category(models.Model):
    title = models.CharField(max_length=255, blank=True)
    ref = models.CharField(max_length=10, blank=True, unique=True)

    class Meta:
        verbose_name_plural = _('Categories')

    def __unicode__(self):
        return self.title or self.ref

class Product(models.Model):
    item_number = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, related_name='products')

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
            ("can_read_all", "Can read all product in one request"),
            ("can_read", "Can read a product property"),
            ("can_see_quantity", "Can see quantity in stock"),
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
