from rest_framework import serializers
from item.models import Category as CategoryModel
from item.models import Item as ItemModel
from item.models import Order as OrderModel
from item.models import ItemOrder as ItemOrderModel

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = '__all__'
        
class ItemSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    def get_category(self, obj):
        return obj.category.name
    class Meta:
        model = ItemModel
        fields = ["name", "category", "image_url"]

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        fields = ["delivery_address", "order_date"]
        
class ItemOrderSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    item = ItemSerializer(read_only=True)
    # 외래키로 접근하는 방식이랑 비슷
    item_name = serializers.ReadOnlyField(source='item.name')
    
    class Meta:
        model = ItemOrderModel
        fields = ["order", "item", "item_count"]