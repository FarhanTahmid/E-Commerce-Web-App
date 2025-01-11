from django.db import models
from django_resized import ResizedImageField
from django.utils import timezone
from inventory.models import *
# Create your models here.

class Product_type(models.Model):
    '''This Table stores all the types of product the business wants to sell'''

    type=models.CharField(null=False,blank=False,max_length=40,verbose_name="Product Type") #The name of the product category, non nullable field
    description=models.CharField(null=False,blank=False,max_length=400,verbose_name="Description of Product Type") #the description of the product type
    
    class Meta:
        verbose_name="Product Type"
        verbose_name_plural="Product Types"

    # def save(self,*args, **kwargs):
    #     if(Product_type.objects.filter(type=self.type).exists()):
    #         raise ValueError("Product Type already exists")
    
    def __str__(self) -> str:
        # returns the type's primary when called via filter or get
        return str(self.pk)


class Product_Category(models.Model):
    '''This Table stores all the categories of product under different types of the product the business wants to sell'''
    
    product_type=models.ForeignKey(Product_type,null=False,blank=False,on_delete=models.CASCADE) #Every category must have product type
    category_name=models.CharField(null=False,blank=False,max_length=40,verbose_name="Product Category")
    description=models.CharField(null=False,blank=False,max_length=400,verbose_name="Description of Product Category")
    
    class Meta:
        verbose_name="Product Category"
        verbose_name_plural="Product Categories"

    def __str__(self) -> str:
        # returns the category pk when called via filter or get
        return str(self.pk)

class Product_Sub_Category(models.Model):
    
    '''This Table stores all the sub-categories of product under different categories of the product the business wants to sell'''
    category_id=models.ManyToManyField(Product_Category) #Every sub category must have product category. It is a many to many relationship
    sub_category_name=models.CharField(null=False,blank=False,max_length=40,verbose_name="Product Sub-Category")
    description=models.CharField(null=False,blank=False,max_length=400,verbose_name="Description of Product Sub-Category")
    
    class Meta:
        verbose_name="Product Sub-Category"
        verbose_name_plural="Product Sub-Categories"

    def __str__(self) -> str:
        # returns the sub-category pk when called via filter or get
        return str(self.pk)

class Product_Brands(models.Model):
    
    '''This table is for storing brand information related to specific product sub categories'''

    brand_name=models.CharField(null=False,blank=False,max_length=100,verbose_name="Brand Name")
    brand_country=models.CharField(null=True,blank=True,max_length=100,verbose_name="Brand Origin Country")
    brand_description=models.TextField(null=True,blank=True,verbose_name="Brand Description")
    brand_established_year=models.IntegerField(null=False,blank=False)
    brand_logo=models.ImageField(null=True,blank=True,upload_to='brand_logos/')
    is_own_brand=models.BooleanField(null=False,blank=False,default=False)
    
    class Meta:
        verbose_name="Brand"
        verbose_name_plural="Brands"

    def __str__(self) -> str:
        return str(self.brand_name)
    

class Product_Colors(models.Model):
    '''This table is for storing color information related to specific products'''
    product_color_code=models.CharField(null=False,blank=False,max_length=50)
    product_color_name=models.CharField(null=False,blank=False,max_length=100)
    
    class Meta:
        verbose_name="Product Color"
        verbose_name_plural="Product Colors"
    
    def __str__(self):
        return str(self.pk)

class Product_Flavours(models.Model):
    '''This table is for storing flavor information related to specific products'''
    product_flavour_name=models.CharField(null=False,blank=False,max_length=100)

    class Meta:
        verbose_name="Product Flavour"
        verbose_name_plural="Product Flavours"
        
    def __str__(self):
        return str(self.pk)
class Product(models.Model):
    '''This table stores the description of Product'''
    
    product_name=models.TextField(null=False,blank=False)
    product_brand=models.ForeignKey(Product_Brands,null=True,blank=True,on_delete=models.CASCADE)
    product_category=models.ManyToManyField(Product_Category)
    product_sub_category=models.ManyToManyField(Product_Sub_Category)
    product_price=models.DecimalField(null=False,blank=False,default=0,max_digits=50,decimal_places=2)
    product_description=models.IntegerField(null=False,blank=False,default=0)
    product_stock_quantity=models.IntegerField(null=False,blank=False,default=0)
    product_ingredients=models.TextField(null=True,blank=True)
    product_usage_direction=models.TextField(null=True,blank=True)
    product_created_at=models.DateTimeField(null=False,blank=False)
    product_colors=models.ManyToManyField(Product_Colors)
    product_flavours=models.ManyToManyField(Product_Flavours)
    
    class Meta:
        verbose_name="Product"
        verbose_name_plural="Products"
        
    def __str__(self) -> str:
        return self.product_name

def get_product_image_path(instance, filename):
    return f'product_images/{instance.product_id}/{filename}'
class Product_Images(models.Model):
    '''This table stores the pictures of the Product. Pictures are stored locally in the product_images/{product_pk}/ folder'''

    product_id=models.ForeignKey(Product,null=False,blank=False,on_delete=models.CASCADE)
    product_image=ResizedImageField(size=[632,632],upload_to=get_product_image_path,blank=True, null=True)
    
    class Meta:
        verbose_name="Product Image"
        verbose_name_plural="Product Images"
    
    def __str__(self):
        return str(self.pk)


class Product_Discount(models.Model):
    '''This table stores all the discounts of the products'''

    DISCOUNT_TYPE_CHOICES=[
        ('percentage','Percentage'),
        ('fixed_amount','Fixed Amount'),
    ]

    discount_type=models.CharField(max_length=30,choices=DISCOUNT_TYPE_CHOICES)
    discount_value=models.DecimalField(max_digits=10,decimal_places=2)
    start_date=models.DateTimeField()
    end_date=models.DateTimeField()
    isActive=models.BooleanField(default=True)
    product_id=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='discounts')

    class Meta:
        verbose_name="Product Discount"
        verbose_name_plural="Product Discounts"

    def __str__(self):
        return f"{self.discount_type} - {self.discount_value}"
    
    # def is_discount_active(self):
    #     '''Check if the discount is currently active'''
    #     now=timezone.now()

    #     if self.start_date <= now and now <= self.end_date and self.isActive:
    #         return True
    #     else:
    #         return False