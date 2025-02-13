from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, ProductViewSet, CategoryViewSet,CustomerViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'customers',CustomerViewSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]