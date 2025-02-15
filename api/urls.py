from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, ProductViewSet, CategoryViewSet,CustomerViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'customers',CustomerViewSet, basename='customers')

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
]