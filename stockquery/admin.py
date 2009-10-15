from django.contrib import admin
from models import StockCheck

class StockCheckAdmin(admin.ModelAdmin):
    search_fields = ('product__item_number', 'user__first_name', 'user__last_name', 'user__username')
    list_display = ('product', 'stock_query', 'ip_address', 'creation_date','interface', 'user')
    list_filter = ('interface', 'creation_date', 'user')

admin.site.register(StockCheck, StockCheckAdmin)
