from django.db import connections
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from django.db.models import Avg
from django.db.utils import OperationalError

from api.auth import Auth0Authentication
from api.models.accounts import User
from .models import Product, Category,Order,Customer
from .serializers import CustomerSerializer, ProductSerializer,OrderSerializer,CategorySerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

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
    authentication_classes = [Auth0Authentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        phone_number = serializer.validated_data.get('phone_number')


        if phone_number:
            existing_customer = Customer.objects.filter(phonenumber=phone_number).first()
            if existing_customer:
                customer = existing_customer
            
        
        else:
            # Create a new customer if no existing one was found
            customer, created = Customer.objects.get_or_create(
                user=user,
                defaults={
                    'name': user.username,  
                    'phonenumber': phone_number or user.phone,
                    'email': user.email
                }
            )

            if not created and customer.phonenumber != phone_number:
                customer.phonenumber = phone_number
                customer.save()

        serializer.save(customer=customer)    


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class HealthCheckView(viewsets.ViewSet): 
    """
    Health check endpoint to verify application and database connectivity
    """
    def get(self, request):
        try:
            connections['default'].cursor()
        except OperationalError:
            return JsonResponse({'status': 'error', 'message': 'Database connection failed'}, status=500)
        
        return JsonResponse({
            'status': 'healthy',
            'message': 'Application is running and database is accessible'
        })
    
#convert this to class
def health_check(request):
    """
    Health check endpoint to verify application and database connectivity
    """
    try:
        connections['default'].cursor()
    except OperationalError:
        return JsonResponse({'status': 'error', 'message': 'Database connection failed'}, status=500)
    
    return JsonResponse({
        'status': 'healthy',
        'message': 'Application is running and database is accessible'
    })   