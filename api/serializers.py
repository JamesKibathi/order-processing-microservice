from rest_framework import serializers

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
    class Meta:
        model = Customer
        fields = ['id',' name ', 'phonenumber', 'email', 'address']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','code', 'title', 'parent']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name', 'description', 'price', 'category']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id','product', 'quantity', 'price']  

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id', 'customer', 'created_at', 'total_amount', 'status', 'items']
    def create(self, validated_data):
        items_data = validated_data.pop('items',[])
        order = Order.objects.create(**validated_data)

        total_amount  = 0
        for item_data in items_data:
            product = item_data['product']
            price = product.price
            quantity = item_data['quantity']
            total_amount  += price * quantity
            OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)

        order.total_amount = total_amount
        order.save()    
        
        return order        