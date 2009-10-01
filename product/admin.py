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

class ImportAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('id', 'title', 'creation_date', 'modification_date', 'is_imported', 'import_date', 'updated_product', 'created_product')
    list_filter = ('is_imported', 'import_date', 'updated_product', 'created_product')
    form = ImportAdminForm
    actions = ('ImportData',)

    def ImportData(self, request, queryset):
        created = 0
        updated = 0
        for import_record in queryset:
            object_dict_list = []
            error_found = False
            f = open(import_record.file.path)
            lines = f.readlines()
            
            positions = {
                'prod_cat': 0,
                'item_no': 1,
                'item_desc': 2,
                'item_desc2': 3,
            }
            
            warehouse_refs = [ e.strip() for e in lines[1].strip().split('|')[1:-1] ][4:]
            warehouses = {}

            for pos, warehouse_ref in enumerate(warehouse_refs, len(positions)):
                warehouses[warehouse_ref], created = Warehouse.objects.get_or_create(ref=warehouse_ref)
                positions[warehouse_ref] = pos
            
            localy_updated = 0
            localy_created = 0
            for line in lines[3:-3]:
                line_data = [ e.strip() for e in line.strip().split('|')[1:-1] ]
                updated = False

                category, created = Category.objects.get_or_create(ref=line_data[positions['prod_cat']])
                product, product_created = Product.objects.get_or_create(category=category, item_number=line_data[positions['item_no']])
                description = "%s %s" % (line_data[positions['item_desc']], line_data[positions['item_desc2']])
                if product_created:
                    localy_created = localy_created + 1
                    product.description = description
                    product.category = category
                    product.save()
                else:
                    if product.description != description:
                        product.description = description
                        updated = True
                    if product.category != category:
                        product.category = category
                        updated = True
                    if updated:
                        product.save()
                
                for warehouse in warehouses.values():
                    inventory, created = Inventory.objects.get_or_create(product=product, warehouse=warehouse)
                    quantity = float(line_data[positions[warehouse.ref]] or 0.0)
                    if inventory.quantity != quantity:
                        updated = True
                        inventory.quantity = quantity
                        inventory.save()

                if updated and not product_created:
                    localy_updated = localy_updated + 1

            import_record.is_imported = True
            import_record.import_date = datetime.now()
            import_record.updated_product = localy_updated
            import_record.created_product = localy_created
            import_record.save()
            updated += localy_updated
            created += localy_created

        self.message_user(request, "%s updated, %s created." % (updated, created))

    ImportData.short_description = "Import Selected records"

admin.site.register(Import, ImportAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
