''' This module contains the admin configurations for the products app '''
from django.contrib import admin
from . import models

class VariationInline(admin.TabularInline):
    ''' Variation inline admin '''
    model = models.Variation
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    ''' Product admin '''
    inlines = [
        VariationInline
    ]

admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Variation)
