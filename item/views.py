from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from item.models import Item as ItemModel
from item.serializers import ItemSerializer

# Create your views here.
class ItemView(APIView):
    def get(self, request):
        all_item = ItemModel.objects.all()
        
        return Response(ItemSerializer(all_item, many=True).data, status=status.HTTP_200_OK)