import pytest

from api.models.accounts import User
from api.models.categories import Category
from api.models.customers import Customer
from api.models.orders import Order

@pytest.mark.django_db
def test_create_customer():
    user = User.objects.create_user(
        email="testuser@example.com",
        password="password123",
        first_name="Test",
        last_name="User"
    )
    customer = Customer.objects.create(user=user, name="Test Customer", phonenumber="1234567890")
    
    assert customer.user.email == "testuser@example.com"
    assert customer.user.first_name == "Test"
    assert customer.user.last_name == "User"
    assert customer.name == "Test Customer"
    assert customer.phonenumber == "1234567890"

@pytest.mark.django_db
def test_create_category():
    parent_category = Category.objects.create(code="ELEC", title="Electronics")
    sub_category = Category.objects.create(code="MOBILE", title="Mobile Phones", parent=parent_category)

    assert sub_category.parent == parent_category
    assert parent_category.children.count() == 1


@pytest.mark.django_db
def test_create_order():
    user = User.objects.create_user(
        email="testuser@example.com",
        password="password123",
        first_name="Test",
        last_name="User"
    )
    customer = Customer.objects.create(user=user, name="Test Customer", phonenumber="1234567890")
    order = Order.objects.create(customer=customer, total_amount=100.50)

    assert order.customer == customer
    assert order.total_amount == 100.50