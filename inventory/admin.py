from django.contrib import admin
from models import Inventory, Warehouse

class InventoryAdmin(admin.ModelAdmin):
    search_fields = ('product__item_number',)
    list_display = ('warehouse', 'product', 'quantity', 'modification_date')
    list_filter = ('warehouse', )

class InventoryInline(admin.TabularInline):
    model = Inventory
    extra = 0

class WarehouseAdmin(admin.ModelAdmin):
    search_fields = ('title', 'ref')
    list_display = ('ref', 'title',)


admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Warehouse, WarehouseAdmin)
