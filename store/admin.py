from django.contrib import admin

from .models import (
    Order,
    Category,
    Product,
    Image,
    Characteristics,
    Command,
)

class ImageInline(admin.TabularInline):
    model = Image
    extra = 0

class CharacteristicsInline(admin.TabularInline):
    model = Characteristics
    extra = 0

class ProductInline(admin.TabularInline):
    model = Product
    extra = 0

class OrderInline(admin.TabularInline):
    model = Order
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'level', 'is_stock', 'is_avtivated', ]
    list_filter = ['level', 'best', 'is_stock', 'is_avtivated', ]
    inlines = [ImageInline, CharacteristicsInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'value', ]
    inlines = [ProductInline, ]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'quantity', 'ordered']
    list_filter = ['user', 'ordered', ]

@admin.register(Command)
class CommanAdmin(admin.ModelAdmin):
    list_display = ['user', 'has_deliver', 'is_sell', 'is_cancel', ]
    list_filter = ['user', ]
    inlines = [OrderInline, ]

