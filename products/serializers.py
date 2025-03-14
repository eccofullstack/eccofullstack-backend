from rest_framework import serializers
from .models import Category,Product,Label

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields= '__all__'

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields= '__all__'

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='name'
    )

    label = serializers.SlugRelatedField(
        many=True, queryset=Label.objects.all(), slug_field='name'
    )