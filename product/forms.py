from django import forms
from django.conf import settings

from models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product

class ProductFormWithoutCategory(ProductForm):
    class Meta(ProductForm.Meta):
        exclude = ('category',)

class ProductFormWithoutCategoryNotMandatory(ProductFormWithoutCategory):
    item_number = forms.CharField(max_length=20, required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)
    title = forms.CharField(max_length=255, required=False) 
    
