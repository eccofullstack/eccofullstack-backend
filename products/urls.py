from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet,ProductViewSet

router = DefaultRouter()
router.register(r'categorias',CategoryViewSet,'categorias')
router.register(r'productos',ProductViewSet,'productos')

urlpatterns = [
    path('',include(router.urls))
]
