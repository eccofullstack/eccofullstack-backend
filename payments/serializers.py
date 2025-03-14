from rest_framework import serializers
from .models import Payment
from orders.models import Order

class PaymentSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())

    class Meta:
        model = Payment
        fields = ["id", "order", "payment_method", "status", "transaction_id", "created_at"]
        read_only_fields = ["id", "status", "created_at"]

    def validate(self, data):
        """Validaciones personalizadas"""
        if Payment.objects.filter(order=data["order"]).exists():
            raise serializers.ValidationError({"order": "Esta orden ya tiene un pago registrado"})
        return data
