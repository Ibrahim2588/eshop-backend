from rest_framework import serializers

from .models import (
    Order,
    Category,
    Product,
    Characteristics,
    Image,
    Command,
)


class CategorySerialiser(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CharacteristicSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Characteristics
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class ProductListSerializer(serializers.ModelSerializer):
    main_image = serializers.ImageField()
    category = CategorySerialiser()
    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'description',
            'level',
            'best',
            'price',
            'disccount',
            'reduction',
            'current_price',
            'main_image',
            'category',
        ]

class ProductDetailSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True,)
    characteristics = CharacteristicSerialiser(many=True, read_only=True,)
    main_image = serializers.ImageField(use_url=True)
    category = CategorySerialiser()
    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'description',
            'price',
            'disccount',
            'reduction',
            'current_price',
            'main_image',
            'category',
            
            'images',
            'characteristics',
        ]

class OrderSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True, read_only=True)
    class Meta:
        model = Order
        fields = [
            'id',
            'product',
            'title',
            'image',
            'quantity',
            'order_price',
            'product_price',
            'ordered',
        ]
        read_only_fields = [
            'id',
            'ordered',
        ]


class CommandSerializer(serializers.ModelSerializer):

    orders = OrderSerializer(many=True, read_only=True,)

    class Meta:
        model = Command
        fields = [
            'id',
            'user',
            'command_code',
            'has_deliver',
            'is_sell',
            'is_cancel',
            'localisation_x',
            'localisation_y',
            'orders',
        ]
        read_only_fields = [
            'id',
            'user',
            'command_code',
        ]