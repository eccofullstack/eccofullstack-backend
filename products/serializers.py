from rest_framework import serializers
from .models import Category, Product, Label
import cloudinary.utils

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def get_image(self, obj):
        """Obtiene la URL correcta de Cloudinary."""
        if obj.image:
            return obj.image.url  # Usa la URL generada por Cloudinary
        return None  # Si no hay imagen, devuelve None

class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()  # Generar URL completa de la imagen

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='name'
    )
    label = serializers.SlugRelatedField(
        many=True, queryset=Label.objects.all(), slug_field='name'
    )

    class Meta:
        model = Product
        fields = '__all__'

    def get_image(self, obj):
        """Obtiene la URL correcta de Cloudinary."""
        if obj.image:
            return obj.image.url  # Usa la URL generada por Cloudinary
        return None  # Si no hay imagen, devuelve None
