'''Admin configuration for the orders app.'''
from django.contrib import admin
from . import models

class OrderItemInline(admin.TabularInline):
    ''' Inline admin for OrderItem model '''
    model = models.OrderItem
    extra = 1
    
class OrderAdmin(admin.ModelAdmin):
    ''' Admin for Order model '''
    inlines = [
        OrderItemInline,
    ]

admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderItem)
