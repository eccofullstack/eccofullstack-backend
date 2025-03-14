from django.db import models
from django.contrib.auth import get_user_model
from shopping_cart.models import ShoppingCart, ShoppingCartItem
from products.models import Product
from django.core.exceptions import ValidationError

User = get_user_model()

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('paid', 'Pagado'),
        ('shipped', 'Enviado'),
        ('delivered', 'Entregado'),
        ('canceled', 'Cancelado'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paypal_order_id = models.CharField(max_length=255, blank=True, null=True)
    def calculate_total(self):
        """Calcula el total de la orden sumando los items."""
        total = sum(item.get_total_price() for item in self.items.all())
        self.total_price = total
        self.save()

    def __str__(self):
        return f"Orden {self.id} - {self.user.username} - {self.get_status_display()}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,editable=False)

    def get_total_price(self):
        """Calcula el precio total del item"""
        return self.quantity * self.price
    
    def save(self, *args, **kwargs):
        # Asignar el precio desde el producto
        self.price = self.product.price  

        # Buscar si ya existe el mismo producto en la orden
        existing_item = OrderItem.objects.filter(order=self.order, product=self.product).exclude(id=self.id).first()

        if existing_item:
            # Si ya existe, aumentar la cantidad y eliminar el duplicado
            existing_item.quantity += self.quantity
            existing_item.save()
            
            # **Eliminar el duplicado en vez de interrumpir**
            self.delete()
        else:
            super().save(*args, **kwargs)  # Guardar el item si no existía antes

        # **Asegurar que siempre se recalcula el total**
        self.order.calculate_total()


    def __str__(self):
        return f"{self.quantity} x {self.product.name} en Orden {self.order.id}"



