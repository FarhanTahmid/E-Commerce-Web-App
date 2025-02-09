from django.db import models
from django_resized import ResizedImageField

# Create your models here.


def get_business_logo_image_path(instance, filename):
    return f'product_images/{instance.product_id.product_name}/{filename}'
class Business_Identity(models.Model):
    '''
    This class stores all the primary identities of the business company. This will be a single row class
    to specify one buisiness in the whole app.
    '''
    platform_product_key=models.CharField(null=False,blank=False,primary_key=True,max_length=200) #Product key will be provided by the mother company
    business_name=models.CharField(null=False,blank=False,max_length=100)
    business_logo=ResizedImageField(size=[632,632],upload_to=get_business_logo_image_path,blank=True, null=True)
    business_description=models.TextField(null=True,blank=True)
    
    class Meta:
        verbose_name="Business Identity"
        verbose_name_plural="Business Identities"
    def __str__(self) -> str:
        return self.business_name

    
    
    