from datetime import timedelta, timezone
from django.shortcuts import get_object_or_404
from django.db.models import F, Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from item.models import Item as ItemModel
from item.models import Category as CategoryModel
from item.models import ItemOrder as ItemOrderModel
from item.serializers import ItemOrderSerializer, ItemSerializer

# Create your views here.
class ItemView(APIView):
    def get(self, request):
        category = request.GET.get('category', None)
        # items = ItemModel.objects.filter(category__name = category)
        # CategoryModel 쿼리셋을 역참조 하여 카테고리와 관련된 아이템들을 한꺼번에 가져옴
        items = CategoryModel.objects.prefetch_related('item_set').get(name=category).item_set.all()
        if items.exists():
            serializer = ItemSerializer(items, many=True)
            return Response(serializer.data)
        
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request):
        item_serializer = ItemSerializer(data=request.data)
        if item_serializer.is_valid():
            # CategoryModel에서, 카테고리 아이디(1번=food)를 get한 걸 category_instance 객체에 넣어줌
            category_instance = get_object_or_404(CategoryModel, id=request.data['category'])
            # ItemModel의 category는 외래키니까 category_instance 객체를 넣어줌
            item_serializer.save(category=category_instance)
            return Response(item_serializer.data, status=status.HTTP_200_OK)
        
        return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ItemOrderView(APIView):
    def get(self, request):
        order_id = self.request.query_params.get('order_id')
        
        data = ItemOrderModel.objects.filter(
            Q(order__order_date__range=[timezone.now() - timedelta(days=7), timezone.now()]) &
            Q(order_id=order_id)
        )
        
        if data.exists():
            serializer = ItemOrderSerializer(data, many=True)
            return Response(serializer.data)
        
        return Response(status=status.HTTP_404_NOT_FOUND)