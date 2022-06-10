from tags.models import TaggedItem
from django.contrib import admin, messages
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models.aggregates import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode
from . import models

class tagInLine(GenericTabularInline):
    model = TaggedItem

class inventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<15', 'Low')
        ]

    def queryset(self, request, queryset):
        if self.value() == '<15':
            return queryset.filter(inventory__lt=15)

class orderItemInLine(admin.TabularInline):
    autocomplete_fields = ['product']
    model = models.Order_item
    extra = 0
    min_num = 1
    max_num = 10

@admin.register(models.Product)
class productAdmin(admin.ModelAdmin):
    inlines = [tagInLine]
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug': ['title']
    }
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price', 'inventory_status', 'collection']
    list_editable = ['unit_price']
    list_per_page = 10
    list_filter = ['collection', 'last_update', inventoryFilter]
    search_fields = ['product']

    # sorting
    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 15:
            return 'Low'
        return "OK"

    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated.', messages.ERROR
        )

@admin.register(models.Customer)
class customerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

@admin.register(models.Order)
class orderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [orderItemInLine]
    list_display = ['id', 'placed_at', 'customer']

@admin.register(models.Collection)
class collectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = reverse('admin:store_product_changelist') + '?' + urlencode({'collection__id': str(collection.id)})
        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count('product'))