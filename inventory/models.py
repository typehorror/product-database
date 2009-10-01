from django.db import models
from django.utils.translation import ugettext_lazy as _

WAREHOUSE_CHOICE = (
    ('CA','California Hawthorn'),
    ('FL','Florida'),
    ('IT','In Transit'),
)

class Warehouse(models.Model):
    ref = models.CharField(max_length=20)
    title = models.CharField(max_length=128, blank=True)
        
    def __unicode__(self):
        return self.title

class Inventory(models.Model):
    warehouse = models.ForeignKey(Warehouse)
    quantity = models.FloatField(default=0.0)
    product = models.ForeignKey('product.product', related_name='inventories')
    modification_date = models.DateTimeField(auto_now=True, auto_now_add=True)
    
    class Meta:
        verbose_name_plural = _('Inventories')
    
    def __unicode__(self):
        return 'Inventory for %s at %s' % (self.product, self.warehouse)
        
