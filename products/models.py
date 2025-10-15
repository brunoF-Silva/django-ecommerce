'''  This module defines the models for products and its variations '''

import os
from django.db import models
from django.conf import settings
from PIL import Image

from django.utils.text import slugify
from utils import utils

class Product(models.Model):
    ''' Product model '''
    name = models.CharField(max_length=255)
    short_description = models.TextField(max_length=255)
    long_description = models.TextField()
    image = models.ImageField(
        upload_to='product_images/%Y/%m', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    marketing_price = models.FloatField(verbose_name="Price")
    promotional_marketing_price = models.FloatField(default=0, verbose_name="Promo Price")
    type = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variable'),
            ('S', 'Simple'),
        )
    )
    
    def get_formatted_price(self):
        ''' Return formatted price '''
        return utils.format_price_usa(self.marketing_price)
    
    get_formatted_price.short_description = 'Price'
    
    def get_formatted_promotional_price(self):
        ''' Return formatted promotional price '''
        return utils.format_price_usa(self.promotional_marketing_price)
    
    get_formatted_promotional_price.short_description = 'Promo Price'

    @staticmethod
    def resize_image(img, new_width=800):
        ''' Resize image to new width '''
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        print(img_full_path)
        
        img_pil = Image.open(img_full_path)
        original_width, original_height = img_pil.size
        
        if original_width <= new_width:
            img_pil.close()
            return
        
        new_height = round((new_width * original_height) / original_width)

        new_img = img_pil.resize(
            (new_width, new_height), Image.Resampling.LANCZOS)
        
        new_img.save(
            img_full_path,
            optimize=True,
            quality=50
        )
        
    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f"{slugify(self.name)}"
            self.slug = slug
        
        super().save(*args, **kwargs)

        max_image_size = 800

        if self.image:
            self.resize_image(self.image, max_image_size)

    def __str__(self):
        return f"{self.name}"
    
class Variation(models.Model):
    ''' Product variation model '''
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    price = models.FloatField()
    promotional_price = models.FloatField(default=0)
    stock = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        print(f"!!!!!!!!!!!!!!{self.product.name}")
        return self.name or self.product.name
    

