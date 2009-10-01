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

    def __unicode__(self):
        return self.item_number

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
