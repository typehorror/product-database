from exceptions import ValueError
import csv
from datetime import datetime


from django.contrib import admin
from django import forms


from models import Inventory, Warehouse, Import
from product.models import Product

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

class ImportAdminForm(forms.ModelForm):
    search_fields = ('title',)
    list_filter = ('is_imported', 'import_date', )
    class Meta:
        exclude = ('is_imported', 'import_date', 'updated_product', 'created_product')

class ImportAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('id', 'title', 'creation_date', 'modification_date', 'is_imported', 'import_date',)
    list_filter = ('is_imported', 'import_date')
    form = ImportAdminForm
    actions = ('ImportInventory',)

    def ImportInventory(self, request, queryset):
        not_created = []
        warehouse_created = 0
        inventory_created = 0
        inventory_updated = 0
        for import_record in queryset:
            object_dict_list = []
            error_found = False

            reader = csv.reader(open(import_record.file.path))
            # The first column is the item_number (we ignore it on the first line)
            # The other columns are inventory place
            warehouse_refs = [ warehouse.strip() for warehouse in reader.next()[1:] if warehouse.strip() ]
            warehouses = []
            for pos, warehouse_ref in enumerate(warehouse_refs):
                warehouse, created = Warehouse.objects.get_or_create(ref=warehouse_ref)
                warehouses.append(warehouse)
                if created:
                    warehouse_created += 1

            for (line, row) in enumerate(reader):
                # try to get the product, if not pass to the other line
                item_number=row[0].strip()
                try:
                    product = Product.objects.get(item_number=item_number)
                except Product.DoesNotExist, e:
                    not_created.append(item_number) 
                    continue
                
                for (positition, quantity) in enumerate(row[1:]):
                    try:
                        quantity = float(quantity)
                    except ValueError, e:
                        # impossible to convert the value to a float, we jump to the other quantity column
                        continue
                    warehouse = warehouses[positition]
                    inventory, created = Inventory.objects.get_or_create(product=product, warehouse=warehouse)                        
                    if inventory.quantity != quantity:
                        if created:
                            inventory_created += 1
                        else:
                            inventory_updated += 1
                        inventory.quantity = quantity
                        inventory.save()

            import_record.is_imported = True
            import_record.import_date = datetime.now()
            import_record.save()

        self.message_user(request, "%s inventories updated, %s inventories created, %s warehouse_created, %s not imported: %s" % (inventory_updated, inventory_created, warehouse_created, len(not_created), ', '.join(not_created) ))

    ImportInventory.short_description = "Import Selected Inventories"

admin.site.register(Import, ImportAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Warehouse, WarehouseAdmin)
