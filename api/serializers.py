from rest_framework import serializers

from api.utils.services import CustomerUserService

from .models import User,Customer, Category, Product, Order, OrderItem

class UserDataSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = [
                   'id', "username", 'first_name', 'last_name', 'email', 'phone', 
                   'is_active', 'is_staff', 'date_joined', 'permissions'
                ]
        read_only_fields = ["id", "is_active", "is_staff", "date_joined"]
    def get_permissions(self, obj):
        return obj.user_permissions.values_list("codename", flat=True)  

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, required=True, min_length=8)
    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email', 'phone', 'password', 'confirm_password'
        ] 
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Password fields didn't match."})
        return data  
    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)  
        user.save()
        return user         
    
class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True) 
    class Meta:
        model = Customer
        fields = ['id','name', 'phonenumber', 'email', 'address','user']
    def create(self, validated_data):
        return Customer.objects.create(**validated_data)

class CategorySerializer(serializers.ModelSerializer):
    code = serializers.CharField(read_only=True)
    class Meta:
        model = Category
        fields = ['id','code', 'title', 'parent']

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all()) 
    class Meta:
        model = Product
        fields = ['id','name', 'description', 'price', 'category']

class OrderItemSerializer(serializers.ModelSerializer):
    price = serializers.ReadOnlyField(source='product.price')
    class Meta:
        model = OrderItem
        fields = ['id','product', 'quantity', 'price']  
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be a positive integer.")
        return value    
    
    def create(self, validated_data):
        # Fetch the price from the related Product model
        product = validated_data['product']
        price = product.price
        validated_data['price'] = price  
        return super().create(validated_data)

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total_amount = serializers.ReadOnlyField()
    status = serializers.ReadOnlyField()
    customer =  CustomerSerializer(read_only=True)
    phone_number = serializers.CharField(write_only=True)
    class Meta:
        model = Order
        fields = ['id', 'customer', 'created_at', 'total_amount', 'status', 'items','phone_number']
    def create(self, validated_data):
        items_data = validated_data.pop('items',[])
        phone_number = validated_data.pop('phone_number')

        total_amount = sum(
            item_data['product'].price * item_data['quantity']
            for item_data in items_data
        )
        

        order = Order.objects.create(**validated_data,total_amount=total_amount)

        # Create order items
        OrderItem.objects.bulk_create([
            OrderItem(
                order=order,
                product=item_data['product'],
                quantity=item_data['quantity'],
                price=item_data['product'].price
            )
            for item_data in items_data
        ])    

        return order        