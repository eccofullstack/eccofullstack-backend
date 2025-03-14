from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import ShoppingCart, ShoppingCartItem
from rest_framework.permissions import IsAuthenticated
from .serializers import ShoppingCartSerializer, ShoppingCartItemSerializer
from products.models import Product

class ShoppingCartViewSet(viewsets.ModelViewSet):
    """ViewSet para manejar el carrito de compras"""
    serializer_class = ShoppingCartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    def list(self, request):
        """Retorna el carrito del usuario autenticado"""
        cart, _ = ShoppingCart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def add_item(self, request):
        """Agregar un producto al carrito sin duplicados"""
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        if quantity <= 0:
            return Response({"error": "Cantidad inválida"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        cart, _ = ShoppingCart.objects.get_or_create(user=request.user)

        # Verifica si el producto ya está en el carrito antes de crearlo
        cart_item, created = ShoppingCartItem.objects.get_or_create(cart=cart, product=product)

        if not created:  # Si ya existe, incrementa la cantidad
            cart_item.amount += quantity  
        else:  # Si no existe, asigna la cantidad inicial
            cart_item.amount = quantity  

        cart_item.save()
        return Response({"message": "Producto agregado correctamente"}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["delete"])
    def clear(self, request):
        """Vaciar el carrito"""
        cart = ShoppingCart.objects.filter(user=request.user).first()
        if cart:
            cart.items.all().delete()
            return Response({"message": "Carrito vaciado"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "Carrito no encontrado"}, status=status.HTTP_404_NOT_FOUND)


class ShoppingCartItemViewSet(viewsets.ModelViewSet):
    """ViewSet para manejar los items del carrito"""
    serializer_class = ShoppingCartItemSerializer

    def get_queryset(self):
        cart = ShoppingCart.objects.filter(user=self.request.user).first()
        return ShoppingCartItem.objects.filter(cart=cart) if cart else ShoppingCartItem.objects.none()

    @action(detail=True, methods=["patch"])
    def update_quantity(self, request, pk=None):
        """Actualizar la cantidad de un producto en el carrito"""
        new_amount = request.data.get("amount")

        if not new_amount or int(new_amount) <= 0:
            return Response({"error": "Cantidad inválida"}, status=status.HTTP_400_BAD_REQUEST)

        cart_item = self.get_object()
        cart_item.amount = int(new_amount)
        cart_item.save()
        return Response({"message": "Cantidad actualizada"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["delete"])
    def remove_item(self, request, pk=None):
        """Eliminar un producto específico del carrito"""
        cart_item = self.get_object()
        cart_item.delete()
        return Response({"message": "Producto eliminado del carrito"}, status=status.HTTP_204_NO_CONTENT)