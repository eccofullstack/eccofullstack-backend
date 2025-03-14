from rest_framework.viewsets import ViewSet
from django.shortcuts import get_object_or_404
from .models import Category,Product
from .serializers import CategorySerializer,ProductSerializer
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class CategoryViewSet(ViewSet):

    def list(self,request):
        queryset = Category.objects.all()
        seializer = CategorySerializer(queryset,many=True)
        return Response(seializer.data,status=status.HTTP_200_OK)
    
    def retrieve(self,request,pk=None):
        category = get_object_or_404(Category,pk=pk)
        serializer= CategorySerializer(category)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def create(self,request):
        category = request.data
        serializer = CategorySerializer(data=category)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def update(self,request,pk=None):
        category = get_object_or_404(Category,pk=pk)
        serializer= CategorySerializer(category,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self,request,pk=None):
        category = get_object_or_404(Category,pk=pk)
        category.delete()
        return Response({"Message":"Categoria Eliminado correctamente"},status=status.HTTP_204_NO_CONTENT)

class ProductViewSet(ViewSet):

    def list(self,request):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
