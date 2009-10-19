from django.contrib import admin
from models import Product, Import, Category
from picture.admin import PictureInline
from inventory.models import Inventory, Warehouse
from inventory.admin import InventoryInline
from django import forms
from datetime import datetime
from django.utils.translation import ugettext_lazy as _

class ProductAdmin(admin.ModelAdmin):
    search_fields = ('title','item_number')
    list_display = ( 'id', 'title', 'item_number', 'category',)
    list_filter = ('category',)
    inlines = (InventoryInline,)

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('ref', 'title',)
    list_display = ( 'ref', 'title',)

class ImportAdminForm(forms.ModelForm):
    search_fields = ('title',)
    list_filter = ('is_imported', 'import_date', )
    class Meta:
        #model = Import
        exclude = ('is_imported', 'import_date', 'updated_product', 'created_product')

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
