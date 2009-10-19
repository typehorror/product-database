from django.contrib import admin
from models import Product, Category
from inventory.models import Inventory, Warehouse
from inventory.admin import InventoryInline
from django.utils.translation import ugettext_lazy as _

class ProductAdmin(admin.ModelAdmin):
    search_fields = ('title','item_number')
    list_display = ( 'id', 'title', 'item_number', 'category',)
    list_filter = ('category',)
    inlines = (InventoryInline,)

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('ref', 'title',)
    list_display = ( 'ref', 'title',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
