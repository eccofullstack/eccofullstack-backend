from rest_framework import serializers
from .models import Blog, Category, Tag

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class BlogSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    author = serializers.StringRelatedField(read_only=True)  # Solo lectura para evitar problemas
    image = serializers.SerializerMethodField()  # Generar URL completa de la imagen


    class Meta:
        model = Blog
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["author"] = request.user  # Asigna automáticamente el usuario autenticado
        return super().create(validated_data)
    
    def get_image(self, obj):
        """Obtiene la URL correcta de Cloudinary."""
        if obj.image:
            return obj.image.url  # Usa la URL generada por Cloudinary
        return None  # Si no hay imagen, devuelve None