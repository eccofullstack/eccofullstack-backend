from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source="product.name")

    class Meta:
        model = OrderItem
        fields = ["id", "product", "product_name", "quantity", "price", "get_total_price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Order
        fields = ["id", "user", "created_at", "status", "total_price", "items"]

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])  
        order = Order.objects.create(**validated_data)  

        for item_data in items_data:
            item_data["order"] = order  
            OrderItem.objects.create(**item_data)  

        order.calculate_total()  
        return order  # ✅ Asegurar que solo se retorne el objeto `order`
