from django.db import models
from customer.models import Customer

# Create your models here.
class Order(models.Model):
    customer_id = models.ForeignKey(Customer, null=False,blank=False,on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(null=False,blank=False,max_digits=10,decimal_places=2)
    shipping_address = models.TextField(null=False,blank=False)
    order_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="Order"
        verbose_name_plural="Orders"
    
    def __str__(self):
        return f"Order by {self.customer_id.full_name}({self.customer_id.unique_id})-{self.order_date}, Order Status: {self.order_status}"