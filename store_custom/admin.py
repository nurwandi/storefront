from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib import admin
from store.admin import productAdmin
from tags.models import TaggedItem
from store.models import Product

class tagInLine(GenericTabularInline):
    search_fields = ['tag']
    autocomplete_fields = ['tag']
    model = TaggedItem

class customeProductAdmin(productAdmin):
    inlines = [tagInLine]

admin.site.unregister(Product)
admin.site.register(Product, customeProductAdmin)
