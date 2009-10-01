from django.db import models

class Picture(models.Model):
    file = models.ImageField(upload_to="product_picture")
    title = models.CharField(max_length=255, blank=True)
    products = models.ManyToManyField('product.Product', related_name='pictures')
