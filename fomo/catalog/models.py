from django.db import models
from polymorphic.models import PolymorphicModel

# Create your models here.

class Category(models.Model):
    #id
    codename = models.TextField(blank=True, null=True, unique=True)
    name = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

#Product
class Product(PolymorphicModel):
    #id
    name = models.TextField(blank=True, null=True)
    #many to one
    category = models.ForeignKey('Category')
    price = models.DecimalField(max_digits=8, decimal_places=2)  #999,999.99
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    picture = models.TextField(blank=True, null=True)
    desc = models.TextField(blank=True, null=True)
    # django screams at you if you try to make an abstract product
    #class Meta:
    #         abstract = True

class ProductPicture(models.Model):
    # DONT USE product_id - because of some reasons
    product = models.ForeignKey(Product)
    path1 = models.TextField(null=True)
    path2 = models.TextField(null=True)
    path3 = models.TextField(null=True)
    path4 = models.TextField(null=True)
    path5 = models.TextField(null=True)

#BulkProducts
class BulkProduct(Product):
    #id
    #name
    #Category
    #price
    #create_date
    #modified_date
    quantity = models.IntegerField()
    reorder_trigger = models.IntegerField()
    reorder_quantity = models.IntegerField()

#UniqueProduct
class UniqueProduct(Product):
    #id
    #name
    #Category
    #price
    #create_date
    #modified_date
    serial_number = models.TextField()

#RentalProduct
class RentalProduct(Product):
    #id
    #name
    #Category
    #price
    #create_date
    #modified_date
    serial_number = models.TextField()
