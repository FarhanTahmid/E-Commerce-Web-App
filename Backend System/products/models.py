from django.db import models
from django_resized import ResizedImageField
from django.utils import timezone
from inventory.models import *
from django.core.validators import MaxValueValidator
from customer.models import Customer
from django_resized import ResizedImageField
import hashlib

# Create your models here.


class Product_Category(models.Model):
    '''This Table stores all the categories of product under different types of the product the business wants to sell'''
    
    category_name=models.CharField(null=False,blank=False,max_length=40,verbose_name="Product Category")
    description=models.TextField(null=False,blank=False,verbose_name="Description of Product Category")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    updated_by = models.JSONField(blank=True, null=True)
    
    class Meta:
        verbose_name="Product Category"
        verbose_name_plural="Product Categories"

    def __str__(self) -> str:
        # returns the category pk when called via filter or get
        return str(self.pk)
    
    def __lt__(self, other):
        return self.category_name < other.category_name

class Product_Sub_Category(models.Model):
    
    '''This Table stores all the sub-categories of product under different categories of the product the business wants to sell'''
    category_id=models.ManyToManyField(Product_Category) #Every sub category must have product category. It is a many to many relationship
    sub_category_name=models.CharField(null=False,blank=False,max_length=40,verbose_name="Product Sub-Category")
    description=models.TextField(null=False,blank=False,verbose_name="Description of Product Sub-Category")
    created_at=models.DateTimeField(auto_now_add=True)#auto saves when the object is created
    updated_at=models.DateTimeField(auto_now=True)#auto updates everytime the object is saved
    updated_by = models.JSONField(blank=True, null=True)
    
    class Meta:
        verbose_name="Product Sub-Category"
        verbose_name_plural="Product Sub-Categories"

    def __str__(self) -> str:
        # returns the sub-category pk when called via filter or get
        return str(self.sub_category_name)
    
    def __lt__(self,other):
        return self.sub_category_name<other.sub_category_name

    
class Product_Brands(models.Model):
    
    '''This table is for storing brand information related to specific product sub categories'''

    brand_name=models.CharField(null=False,blank=False,max_length=100,verbose_name="Brand Name")
    brand_country=models.CharField(null=True,blank=True,max_length=100,verbose_name="Brand Origin Country")
    brand_description=models.TextField(null=True,blank=True,verbose_name="Brand Description")
    brand_established_year=models.IntegerField(null=False,blank=False)
    brand_logo=ResizedImageField(size=[244,244],null=True,blank=True,upload_to='brand_logos/')
    is_own_brand=models.BooleanField(null=False,blank=False,default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    updated_by = models.JSONField(blank=True, null=True)
    
    class Meta:
        verbose_name="Brand"
        verbose_name_plural="Brands"

    def __str__(self) -> str:
        return str(self.brand_name)
    

class Product_Flavours(models.Model):
    '''This table is for storing flavor information related to specific products'''
    product_flavour_name=models.CharField(null=False,blank=False,max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    updated_by = models.JSONField(blank=True, null=True)

    class Meta:
        verbose_name="Product Flavour"
        verbose_name_plural="Product Flavours"
        
    def __str__(self):
        return str(self.pk)
    
    def __lt__(self,other):
        return self.product_flavour_name<other.product_flavour_name

class Product(models.Model):
    '''This table stores the description of Product'''
    
    product_name=models.TextField(null=False,blank=False)
    product_brand=models.ForeignKey(Product_Brands,null=True,blank=True,on_delete=models.CASCADE)
    product_category=models.ManyToManyField(Product_Category,related_name='products')
    product_sub_category=models.ManyToManyField(Product_Sub_Category,related_name='products')
    product_description=models.TextField(null=False,blank=False)
    product_summary=models.TextField(null=False,blank=False)
    product_ingredients=models.TextField(null=True,blank=True)
    product_usage_direction=models.TextField(null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    updated_by = models.JSONField(blank=True, null=True)
    
    class Meta:
        verbose_name="Product"
        verbose_name_plural="Products"
        
    def __str__(self) -> str:
        return self.product_name
    
    def __lt__(self,other):
        return self.product_name< other.product_name
    

class Product_SKU(models.Model):

    product_id = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    product_sku = models.CharField(null=False, blank=False, max_length=100,unique=True)
    product_color = models.CharField(null=True, blank=True, max_length=100)
    product_size = models.CharField(null=True, blank=True, max_length=100)
    product_price=models.DecimalField(null=False,blank=False,default=0,max_digits=50,decimal_places=2)
    product_stock = models.IntegerField(null=False, blank=False, default=0)
    product_flavours=models.ManyToManyField(Product_Flavours,related_name='product_flavour')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    updated_by = models.JSONField(blank=True, null=True)

    class Meta:
        verbose_name="Product SKU"
        verbose_name_plural="Products SKU"

    def generate_and_save_sku(self):
        # Filter existing SKUs with the same product, color, and size
        existing_skus = Product_SKU.objects.filter(
            product_id=self.product_id,
            product_color=self.product_color,
            product_size=self.product_size
        ).count()
        
        sequential_number = existing_skus + 1

        product_name = self.product_id.product_name.replace(' ', '_')
        base_sku = f"{product_name.upper()}_{self.product_color.upper() if self.product_color else 'no_color'.upper()}_{self.product_size.upper() if self.product_size else 'no_size'.upper()}_{sequential_number}"
        unique_hash = hashlib.md5(base_sku.encode()).hexdigest()[:6]
        self.product_sku = f"{base_sku}_{unique_hash.upper()}"

    def save(self, *args, **kwargs):
        #if newly created only then
        if not self.pk or self._is_sku_related_field_updated():
            self.generate_and_save_sku()
        
        super(Product_SKU, self).save(*args, **kwargs)
    
    def _is_sku_related_field_updated(self):
        """Check if fields affecting SKU generation have been updated."""
        if not self.pk:
            return False

        # Get the current state from the database
        current = Product_SKU.objects.get(pk=self.pk)
        return (
            current.product_color != self.product_color or
            current.product_size != self.product_size
        )
    

    def __str__(self) -> str:
        return f"pk:{self.pk} - {self.product_id.product_name}, sku - {self.product_sku}"


def get_product_image_path(instance, filename):
    return f'product_images/{instance.product_id.product_name}/{filename}'
class Product_Images(models.Model):
    '''This table stores the pictures of the Product. Pictures are stored locally in the product_images/{product_pk}/ folder'''

    product_id=models.ForeignKey(Product,null=False,blank=False,on_delete=models.CASCADE)
    product_image=ResizedImageField(size=[632,632],upload_to=get_product_image_path,blank=True, null=True)
    color = models.CharField(null=True, blank=True, max_length=100)
    size = models.CharField(null=True, blank=True, max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    updated_by = models.JSONField(blank=True, null=True)
    
    class Meta:
        verbose_name="Product Image"
        verbose_name_plural="Product Images"
    
    def __str__(self):
        return str(self.product_id.product_name)
    
def get_product_video_path(instance, filename):
    return f'product_videos/{instance.product_id.product_name}/{filename}'
class Product_Videos(models.Model):
    '''This table stores the videos of the Product. Videos are stored locally in the product_videos/{product_pk}/ folder'''

    product_id=models.ForeignKey(Product,null=False,blank=False,on_delete=models.CASCADE)
    product_videos=models.FileField(upload_to = get_product_video_path,blank=True, null=True)
    color = models.CharField(null=False, blank=False, max_length=100)
    size = models.CharField(null=False, blank=False, max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    updated_by = models.JSONField(blank=True, null=True)
    
    class Meta:
        verbose_name="Product Video"
        verbose_name_plural="Product Videos"
    
    def __str__(self):
        return str(self.product_id.product_name)
    
class Product_Discount(models.Model):
    ''''This table stores all the discounts of a product'''

    product_id = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    discount_name = models.CharField(null=False, blank=False, max_length=100)
    discount_amount = models.DecimalField(null=False, blank=False, max_digits=10, decimal_places=2)
    start_date = models.DateTimeField(null=False, blank=False)
    end_date = models.DateTimeField(null=False, blank=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    updated_by = models.JSONField(blank=True, null=True)

    class Meta:
        verbose_name="Product Discount"
        verbose_name_plural="Product Discounts"

    def __str__(self):
        return f"{self.product_id.product_name} - {self.discount_amount}"
    
    def is_discount_active(self):

        '''Check if the discount is currently active'''
        now = timezone.now()
        if self.start_date <= now and now <= self.end_date:
            return True
        else:
            return False
    
class Product_Review(models.Model):

    ''''This table stores all the reviews of a product'''

    product_id = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customer, null=False, blank=False, on_delete=models.CASCADE)
    product_review = models.TextField(null=False, blank=False)
    product_rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)], null=False, blank=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    updated_by = models.JSONField(blank=True, null=True)

    class Meta:
        verbose_name="Product Review"
        verbose_name_plural="Product Reviews"

    def __str__(self):
        return f"{self.product_id.product_name} by {self.customer_id.full_name}"
    


# class Product_Discount(models.Model):
#     '''This table stores all the discounts of the products'''

#     DISCOUNT_TYPE_CHOICES=[
#         ('percentage','Percentage'),
#         ('fixed_amount','Fixed Amount'),
#     ]

#     discount_type=models.CharField(max_length=30,choices=DISCOUNT_TYPE_CHOICES)
#     discount_value=models.DecimalField(max_digits=10,decimal_places=2)
#     start_date=models.DateTimeField()
#     end_date=models.DateTimeField()
#     isActive=models.BooleanField(default=True)
#     product_id=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='discounts')

#     class Meta:
#         verbose_name="Product Discount"
#         verbose_name_plural="Product Discounts"

#     def __str__(self):
#         return f"{self.discount_type} - {self.discount_value}"
    
    # def is_discount_active(self):
    #     '''Check if the discount is currently active'''
    #     now=timezone.now()

    #     if self.start_date <= now and now <= self.end_date and self.isActive:
    #         return True
    #     else:
    #         return False