import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from api.models.accounts import User
from api.models.categories import Category
from api.models.customers import Customer
from api.models.products import Product


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_list_products(api_client):
    category = Category.objects.create(code="ELEC", title="Electronics")
    Product.objects.create(name="Laptop", description="Gaming Laptop", price=1500.00, category=category)

    url = reverse("api:products-list") 
    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1  
    assert response.data[0]["name"] == "Laptop"
    assert response.data[0]["price"] == "1500.00"

@pytest.mark.django_db
def test_create_order(api_client):
   
    user = User.objects.create_user(
        email="testuser@example.com",
        password="password123",
        first_name="Test",
        last_name="User",
        phone="1234567890"
    )
    api_client.force_authenticate(user)

    customer = Customer.objects.create(user=user, name="Test Customer", phonenumber="1234567890")

    category = Category.objects.create(code="ELEC", title="Electronics")
    product = Product.objects.create(name="Laptop", description="Gaming Laptop", price=1500.00, category=category)

    order_data = {
        "customer": customer.id, 
        "items": [{"product": product.id, "quantity": 1}],
        "phone_number": "1234567890"
    }

  
    url = reverse("api:orders-list")  
    response = api_client.post(url, order_data, format="json")

    assert response.status_code == 201
    assert response.data["total_amount"] == "1500.00"
    assert response.data["customer"]["phonenumber"] == "1234567890"
