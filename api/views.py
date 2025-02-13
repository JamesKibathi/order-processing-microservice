from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import Avg
from .models import Product, Category,Order
from .serializers import ProductSerializer,OrderSerializer,CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=['get'])
    def average_price(self, request):
        category_id = request.query_params.get('category_id')
        if not category_id:
            return Response({"error": "Category ID is required"}, 
                          status=status.HTTP_400_BAD_REQUEST)
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        
        subcategories = category.get_descendants(include_self=True)
        avg_price = Product.objects.filter(category__in=subcategories).aggregate(avg_price=Avg('price'))['avg_price']

        return Response({'category_id': category_id, 'average_price': avg_price or 0}) 


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().prefetch_related('items__product')
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer