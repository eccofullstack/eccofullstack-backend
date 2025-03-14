from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from .serializers import OrderSerializer
from shopping_cart.models import ShoppingCart
from products.models import Product
from payments.paypal_service import create_order, capture_paypal_order

class OrderViewSet(viewsets.ModelViewSet):
    """ViewSet para manejar las órdenes de compra con PayPal"""
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Devuelve solo las órdenes del usuario autenticado"""
        return Order.objects.filter(user=self.request.user)

    @action(detail=False, methods=["post"])
    def create_order(self, request):
        """Crea una orden en la base de datos y en PayPal"""
        if not request.user.is_authenticated:
            return Response({"error": "Usuario no autenticado"}, status=status.HTTP_401_UNAUTHORIZED)

        items_data = request.data.get("items", [])
        if not items_data:
            return Response({"error": "No se enviaron productos"}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(user=request.user)
        productos_paypal = []
        total_price = 0  

        for item_data in items_data:
            product_name = item_data.get("product")
            quantity = int(item_data.get("quantity", 1))  # Asegurar que la cantidad sea un número entero

            if quantity <= 0:
                return Response({"error": f"Cantidad inválida para el producto {product_name}"}, status=status.HTTP_400_BAD_REQUEST)

            # Buscar el producto en la base de datos
            product = Product.objects.filter(name=product_name).first()
            if not product:
                return Response({"error": f"Producto '{product_name}' no encontrado"}, status=status.HTTP_404_NOT_FOUND)

            # Crear el OrderItem con la cantidad correcta
            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )

            subtotal = product.price * quantity
            total_price += subtotal

            productos_paypal.append({
                "name": product.name,
                "unit_amount": {"currency_code": "USD", "value": str(round(product.price, 2))},
                "quantity": quantity  # Aquí se usa la cantidad correcta
            })

        order.total_price = total_price
        order.save()

        paypal_response = create_order(productos_paypal, total_price)

        if not paypal_response:
            return Response({"error": "No se recibió respuesta de PayPal"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if paypal_response.get("id"):
            order.paypal_order_id = paypal_response["id"]
            order.save()
            return Response(paypal_response, status=status.HTTP_201_CREATED)

        return Response({"error": "Error al crear orden en PayPal", "paypal_response": paypal_response}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @action(detail=True, methods=["patch"])
    def update_status(self, request, pk=None):
        """Actualiza el estado de la orden"""
        order = self.get_object()
        new_status = request.data.get("status")

        if new_status not in dict(Order.STATUS_CHOICES):
            return Response({"error": "Estado inválido"}, status=status.HTTP_400_BAD_REQUEST)

        order.status = new_status
        order.save()
        return Response({"message": "Estado actualizado correctamente", "order": OrderSerializer(order).data})

    @action(detail=False, methods=["post"], url_path="capture_payment/(?P<paypal_order_id>[^/.]+)")
    def capture_payment(self, request, paypal_order_id=None):
        """Captura el pago usando el ID de PayPal"""
        try:
            order = Order.objects.get(paypal_order_id=paypal_order_id)
        except Order.DoesNotExist:
            return Response({"error": "Orden no encontrada con ese PayPal ID"}, status=status.HTTP_404_NOT_FOUND)

        paypal_response = capture_paypal_order(order.paypal_order_id)

        if not paypal_response:
            return Response({"error": "No se recibió respuesta de PayPal"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        print("📦 Respuesta de PayPal:", paypal_response)

        if paypal_response.get("status") == "COMPLETED":
            order.status = "paid"
            order.save()
            return Response({"message": "Pago capturado exitosamente", "order": OrderSerializer(order).data}, status=status.HTTP_200_OK)

        return Response({"error": "Error al capturar el pago en PayPal", "paypal_response": paypal_response}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
