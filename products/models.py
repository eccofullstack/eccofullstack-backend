from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.
class Category(models.Model):
    name = models.CharField('Name',max_length=50,blank=True,null=True)
    description= models.TextField('Description')
    image = CloudinaryField('image', folder='products/categories/images', blank=True)


    def __str__(self):
        return self.name

class Label(models.Model):
    name = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField('Name', max_length=50,blank=False,null=False)
    description = models.TextField('Description')
    price = models.DecimalField('Price', max_digits=1000, decimal_places=2)
    stock = models.IntegerField('Stock')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = CloudinaryField('image', folder='products/images')  # 🟢 CAMBIO AQUÍ
    creation_date =models.DateTimeField(auto_now=True)
    assessment = models.DecimalField(max_digits=2,decimal_places=1, default=0.0)
    label = models.ManyToManyField(Label,blank=True)

    def __str__(self):
        return self.name