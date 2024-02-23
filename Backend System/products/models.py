from django.db import models
from django_resized import ResizedImageField
from inventory.models import *
# Create your models here.

class Product_type(models.Model):
    '''This Table stores all the types of product the business wants to sell'''
    
    type=models.CharField(null=False,blank=False,max_length=400,verbose_name="Product Type") #The name of the product category, non nullable field
    
    class Meta:
        verbose_name="Product Type"
    
    def __str__(self) -> str:
        # returns the type name when called via filter or get
        return self.type


class Product_Category(models.Model):
    '''This Table stores all the categories of product under different types of the product the business wants to sell'''
    
    type=models.ForeignKey(Product_type,null=False,blank=False,on_delete=models.CASCADE)
    category=models.CharField(null=False,blank=False,max_length=400,verbose_name="Product Category")
    
    class Meta:
        verbose_name="Product Category"
    
    def __str__(self) -> str:
        # returns the category when called via filter or get
        return self.category

class Product_Sub_Category(models.Model):
    
    '''This Table stores all the sub-categories of product under different categories of the product the business wants to sell'''
    category=models.ForeignKey(Product_Category,null=False,blank=False,on_delete=models.CASCADE)
    sub_category=models.CharField(null=False,blank=False,max_length=400,verbose_name="Product Sub-Category")
    
    class Meta:
        verbose_name="Product Sub-Category"
    
    def __str__(self) -> str:
        # returns the sub-category when called via filter or get
        return self.sub_category

class Product_Brands(models.Model):
    
    '''This table is for storing brand information related to specific product sub categories'''

    brand_name=models.CharField(null=False,blank=False,max_length=300)
    brand_logo=models.ImageField(null=True,blank=True,upload_to='brand_logos/')
    brand_description=models.TextField(null=True,blank=True)
    brand_origin=models.CharField(null=True,blank=True,max_length=200)
    
    class Meta:
        verbose_name="Brand Informations"
    
    def __str__(self) -> str:
        return self.brand_name


    
    
class Product(models.Model):
    
    '''This table stores the description of Product'''
    
    product_name=models.TextField(null=False,blank=False)
    product_brand=models.ForeignKey(Product_Brands,null=True,blank=True,on_delete=models.CASCADE)
    product_stock_status=models.ForeignKey(Product_Stock_Status,null=False,blank=False,on_delete=models.CASCADE,default=0)
    product_price=models.IntegerField(null=False,blank=False,default=0)
    product_offer_price=models.IntegerField(null=False,blank=False,default=0)
    
    
    class Meta:
        verbose_name="Product"
    def __str__(self) -> str:
        return self.product_name
    
