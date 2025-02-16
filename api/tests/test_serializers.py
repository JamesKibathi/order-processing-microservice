import pytest
from rest_framework.exceptions import ValidationError
from api.models.categories import Category
from api.serializers import OrderItemSerializer, ProductSerializer


@pytest.mark.django_db
def test_product_serializer():
    category = Category.objects.create(code="ELEC", title="Electronics")
    product_data = {"name": "Laptop", "description": "Gaming Laptop", "price": 1500.00, "category": category.id}

    serializer = ProductSerializer(data=product_data)
    assert serializer.is_valid()
    assert serializer.validated_data["name"] == "Laptop"


@pytest.mark.django_db
def test_order_item_quantity_validation():
    invalid_data = {"product": 1, "quantity": 0}  
    serializer = OrderItemSerializer(data=invalid_data)

    with pytest.raises(ValidationError) as exc:
        serializer.is_valid(raise_exception=True)

    assert "Quantity must be a positive integer." in str(exc.value)