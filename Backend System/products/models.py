from django.db import models

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

class Product(models.Model):
    
    '''This table stores the description of Product'''
    
    product_name=models.TextField(null=False,blank=False)
    
    class Meta:
        verbose_name="Product"
    def __str__(self) -> str:
        return self.product_name
    
