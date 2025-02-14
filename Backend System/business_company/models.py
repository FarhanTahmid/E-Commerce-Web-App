from django.db import models

# Create your models here.

class Business_Identity(models.Model):
    '''
    This class stores all the primary identities of the business company. This will be a single row class
    to specify one buisiness in the whole app.
    '''
    platform_product_key=models.CharField(null=False,blank=False,primary_key=True,max_length=200) #Product key will be provided by the mother company
    business_name=models.CharField(null=False,blank=False,max_length=100)
    business_logo=models.ImageField(null=True,blank=True,upload_to="company_files/identity/")
    business_description=models.TextField(null=True,blank=True)
    
    class Meta:
        verbose_name="Business Identity"
        verbose_name_plural="Business Identities"
    def __str__(self) -> str:
        return self.business_name

    
    
    