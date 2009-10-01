from django.db import models

class Document(models.Model):
    file = models.FileField(upload_to="product_document")
    title = models.CharField(max_length=255, blank=True)
    products = models.ManyToManyField('product.Product', related_name='documents')

    def __unicode__(self):
        return u'Document %s' % (self.title or self.id)

