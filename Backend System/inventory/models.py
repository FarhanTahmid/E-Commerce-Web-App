from django.db import models

# Create your models here.

class Product_Stock_Status(models.Model):
    
    status_type=models.CharField(null=False,blank=False,max_length=100) #In Stock/Out of stock etc.
    
    class Meta:
        verbose_name= "Product Status"
    
    def __str__(self) -> str:
        return self.status_type

    