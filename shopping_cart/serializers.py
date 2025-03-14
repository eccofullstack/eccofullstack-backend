from rest_framework import serializers
from .models import ShoppingCart, ShoppingCartItem
from products.serializers import ProductSerializer  # Importa el serializador del producto

class ShoppingCartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # Mostrar detalles del producto

    class Meta:
        model = ShoppingCartItem
        fields = ["id", "product", "amount", "date_added"]  # Incluye los datos relevantes

class ShoppingCartSerializer(serializers.ModelSerializer):
    items = ShoppingCartItemSerializer(many=True, read_only=True)  # Serializar la lista de items completos

    class Meta:
        model = ShoppingCart
        fields = ["id", "user", "items"]  # Ahora "items" contendrá la info detallada
