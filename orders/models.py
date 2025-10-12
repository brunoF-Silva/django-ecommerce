'''Models for Orders and Order Items in an e-commerce application.'''
from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    ''' Order model '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField()
    status = models.CharField(
        default="C",
        max_length=1,
        choices=(
            ('A', 'Approved'),
            ('C', 'Created'),
            ('R', 'Rejected'),
            ('P', 'Pending'),
            ('S', 'Shipped'),
            ('D', 'Delivered'),
        )
    )
    
    def __str__(self):
        return f"Order N. {self.pk}"

class OrderItem(models.Model):
    ''' Order Item model '''
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.CharField(max_length=255)
    product_id = models.PositiveIntegerField()
    variation = models.CharField(max_length=255)
    variation_id = models.PositiveIntegerField()
    price = models.FloatField()
    price_promo = models.FloatField(default=0)
    quantity = models.PositiveIntegerField()
    image = models.CharField(max_length=2000)
    
    def __str__(self):
        return f"Item from {self.order}"
    class Meta:
        ''' Meta class for OrderItem '''
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'