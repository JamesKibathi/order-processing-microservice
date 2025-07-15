from django.db import connections
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from django.db.models import Avg, Count
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
    def by_category(self, request):
        """
        Get products filtered by category, including products in subcategories
        """
        category_id = request.query_params.get('category_id')
        if not category_id:
            return Response(
                {"error": "Category ID is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            category = Category.objects.get(id=category_id)
          
            subcategories = category.get_descendants(include_self=True)
            
            products = Product.objects.filter(category__in=subcategories)
            
            serializer = self.get_serializer(products, many=True)
            return Response(serializer.data)
        
        except Category.DoesNotExist:
            return Response(
                {"error": "Category not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['get'])
    def average_price(self, request):
        """
        Calculate average price for a category and its subcategories
        """
        category_id = request.query_params.get('category_id')
        if not category_id:
            return Response({"error": "Category ID is required"}, 
                          status=status.HTTP_400_BAD_REQUEST)
        try:
            category = Category.objects.get(id=category_id)
            subcategories = category.get_descendants(include_self=True)

            avg_price = Product.objects.filter(
                category__in=subcategories
            ).aggregate(avg_price=Avg('price'))['avg_price']

            return Response({
                'category_id': category_id, 
                'category_title': category.title,
                'average_price': avg_price or 0,
                'total_products': Product.objects.filter(category__in=subcategories).count()
            })

        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    

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

    def get_queryset(self):
       
        return Category.objects.annotate(
            products_count=Count('product', distinct=True)
        )
    
    @action(detail=False, methods=['get'])
    def root_categories(self, request):
        """
        Retrieve all root-level categories
        """
        root_categories = Category.get_root_categories()
        serializer = self.get_serializer(root_categories, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def hierarchy(self, request, pk=None):
        """
        Retrieve the full category hierarchy starting from a specific category
        """
        try:
            category = self.get_object()
            context = {'depth': 0}
            serializer = self.get_serializer(category, context=context)
            return Response(serializer.data)
        except Category.DoesNotExist:
            return Response(
                {"error": "Category not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

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