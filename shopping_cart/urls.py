from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShoppingCartViewSet, ShoppingCartItemViewSet

router = DefaultRouter()
router.register(r'cart', ShoppingCartViewSet, basename="cart")
router.register(r'cart/item', ShoppingCartItemViewSet, basename="cart_item")

urlpatterns = [
    path('', include(router.urls)),
]
