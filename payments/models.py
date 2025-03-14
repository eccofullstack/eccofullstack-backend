from django.db import models
from orders.models import Order

class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('completed', 'Completado'),
        ('failed', 'Fallido'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('paypal', 'PayPal'),
        ('stripe', 'Stripe'),
        ('transfer', 'Transferencia'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment", unique=True)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pago {self.transaction_id or 'N/A'} - {self.get_status_display()}"
