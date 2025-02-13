from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import Avg
from .models import Product, Category
from .serializers import ProductSerializer

# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=['get'])
    def category_average(self, request):
        category_id = request.query_params.get('category_id')
        if not category_id:
            return Response({"error": "Category ID is required"}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        #Get all subcategories
        category = Category.objects.get(id=category_id)
        subcategories = category.get_descendants(include_self=True)

        #calculate average price for each subcategory
        avg_price = Product.objects.filter(category__in=subcategories).aggregate(avg_price=Avg('price'))['avg_price']
        return Response({'category_id': category_id,'average_price': avg_price})

