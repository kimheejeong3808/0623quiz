from rest_framework import serializers
from item.models import Category as CategoryModel
from item.models import Item as ItemModel
from item.models import Order as OrderModel
from item.models import ItemOrder as ItemOrderModel

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ["name"]
        
class ItemSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    def get_category(self, obj):
        return [category.id for category in obj.category.all()]
    class Meta:
        model = ItemModel
        fields = ["name", "category", "image_url"]

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        fields = ["delivery_address", "order_date", "item"]
        
class ItemOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemOrderModel
        fields = ["orders", "item", "item_count"]