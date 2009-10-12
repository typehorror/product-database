from django.db import models

ACCESS_TYPE_CHOICE = (
    ('web', 'Web Interface'),
    ('rest', 'REST Interface'),
)

class StockCheck(models.Model):
    """
    An import contains a list of product
    """
    user = models.ForeignKey('auth.User')
    product = models.ForeignKey('product.Product')
    stock_query = models.FloatField()
    ip_address = models.IPAddressField()
    creation_date = models.DateTimeField(auto_now_add=True)
    interface = models.CharField(max_length=4, choices=ACCESS_TYPE_CHOICE)
