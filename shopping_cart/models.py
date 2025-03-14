from django.db import models
from users.models import User
from products.models import Product
from django.db.models.signals import post_save 
from django.dispatch import receiver





# Create your models here.
class ShoppingCart(models.Model):
    
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def add_product(self,product,quantity=1):

        if quantity <= 0:
            return None  # Evita agregar cantidades inválidas

        cart_item,created = ShoppingCartItem.objects.get_or_create(cart=self,product=product)

        if not created:
            cart_item.amount += quantity
        else:
            cart_item.amount = quantity
        
        cart_item.save()
        
        return cart_item


    def __str__(self):
        return self.user.username
    

class ShoppingCartItem(models.Model):
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now=True)


    class Meta:
        unique_together = ('cart', 'product')  # Asegura que no haya duplicados en la BD

    def save(self, *args, **kwargs):
        """Evita duplicados y suma la cantidad si el producto ya está en el carrito."""
        if self.pk:  # Si el objeto ya existe, es una actualización normal
            super().save(*args, **kwargs)
            return

        # Si es un nuevo objeto, verificamos si ya existe uno igual en la base de datos
        existing_item = ShoppingCartItem.objects.filter(cart=self.cart, product=self.product).first()

        if existing_item:
        # En lugar de llamar a save(), usamos update() para evitar la recursión
            ShoppingCartItem.objects.filter(id=existing_item.id).update(amount=existing_item.amount + self.amount)
        else:
            super().save(*args, **kwargs)  # Solo guarda si el producto no existe en el carrito

    def __str__(self):
        return f"{self.amount} x {self.product.name} en carrito de {self.cart.user}"