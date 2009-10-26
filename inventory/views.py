from exceptions import ValueError
import csv
from datetime import datetime
from django.contrib.admin.views.decorators import staff_member_required


from models import Import, Warehouse, Inventory
from product.models import Product
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404


@staff_member_required
def import_inventory(request, object_id):
    import_record = get_object_or_404(Import, pk=object_id)
    
    # reset inventory models if import need it
    if import_record.reset_data:
        # deleting the warehouse will delete the inventories linked to it
        Warehouse.objects.all().delete()

    not_created = []
    warehouse_created = 0
    inventory_created = 0
    inventory_updated = 0
    already_existing = 0
    error_found = False

    reader = csv.reader(open(import_record.file.path))
    # The first column is the item_number (we ignore it on the first line)
    # The other columns are inventory places
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
                # default quantity to 0
                quantity = 0
            warehouse = warehouses[positition]
            if import_record.reset_data:
                # direct creation will speed up the process
                inventory = Inventory.objects.create(product=product, warehouse=warehouse, quantity=quantity)
                inventory_created += 1
            else:
                inventory, created = Inventory.objects.get_or_create(product=product, warehouse=warehouse)                        
                if inventory.quantity != quantity:
                    if created:
                        inventory_created += 1
                    else:
                        inventory_updated += 1
                    inventory.quantity = quantity
                    inventory.save()
                else:
                    already_existing += 1

    import_record.is_imported = True
    import_record.import_date = datetime.now()
    import_record.products_not_found = ', '.join(not_created)
    import_record.save()
    request.user.message_set.create(message='%s inventories updated, %s inventories created, %s warehouse created, %s product not found, %s already existing records' % \
        (inventory_updated, inventory_created, warehouse_created, len(not_created), already_existing))
    return HttpResponseRedirect('/admin/inventory/import/%s' % object_id)    
 

