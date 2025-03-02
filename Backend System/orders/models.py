from django.db import models
from customer.models import Accounts,Coupon
from products.models import Product_SKU
from business_admin.models import BusinessAdminUser

class DeliveryTime(models.Model):

    delivery_name = models.CharField(max_length=1000,null=False,blank=False)
    estimated_delivery_time = models.CharField(max_length=1000,null=False,blank=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    updated_by = models.JSONField(blank=True, null=True)

    class Meta:
        verbose_name = "Delivery Time"

    def __str__(self):
        return str(self.delivery_name)

class Order(models.Model):
    """
    Represents an order placed by a customer in the e-commerce system.

    Attributes:
        order_id (CharField): A unique identifier for the order, generated by the system.
        customer_id (ForeignKey): A reference to the customer who placed the order.
        order_date (DateTimeField): The date and time when the order was created.
        total_amount (DecimalField): The total amount of the order.
        order_status (CharField): The current status of the order (e.g., pending, shipped).
        created_at (DateTimeField): The timestamp when the order record was created.
        updated_at (DateTimeField): The timestamp when the order record was last updated.
        updated_by (ForeignKey): A reference to the admin user who last updated the order.

    Meta:
        verbose_name (str): A human-readable name for the model (singular).
        verbose_name_plural (str): A human-readable name for the model (plural).
    """
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('returned', 'Returned'),
        ('refunded', 'Refunded'),
        ('success','Success'),
    ]
    
    order_id = models.CharField(max_length=100, unique=True, null=False, blank=False)
    customer_id = models.ForeignKey(Accounts, on_delete=models.CASCADE, null=False, blank=False)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_time = models.ForeignKey(DeliveryTime,on_delete=models.CASCADE,related_name='delivery_time')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending', null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.JSONField(blank=True, null=True)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return self.order_id


class OrderDetails(models.Model):
    """
    Represents the details of individual products within an order.

    Attributes:
        order_id (ForeignKey): A reference to the related order.
        product_sku (ForeignKey): A reference to the product SKU included in the order.
        quantity (PositiveIntegerField): The quantity of the product ordered.
        units (PositiveIntegerField): The number of units per item.
        subtotal (DecimalField): The subtotal cost for this product in the order.
        created_at (DateTimeField): The timestamp when the record was created.
        updated_at (DateTimeField): The timestamp when the record was last updated.

    Meta:
        verbose_name (str): A human-readable name for the model (singular).
        verbose_name_plural (str): A human-readable name for the model (plural).
    """
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, null=False, blank=False,related_name="items")
    product_sku = models.ForeignKey(Product_SKU, on_delete=models.CASCADE, null=False, blank=False)
    quantity = models.PositiveIntegerField(null=False, blank=False)
    units = models.PositiveIntegerField(null=False, blank=False, default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.JSONField(blank=True, null=True)

    class Meta:
        verbose_name = "Order Detail"
        verbose_name_plural = "Order Details"

    def __str__(self):
        return str(self.pk)


class OrderShippingAddress(models.Model):
    """
    Stores the shipping address details for an order.

    Attributes:
        order_id (ForeignKey): A reference to the related order.
        address_line1 (CharField): The first line of the shipping address.
        address_line2 (CharField): The second line of the shipping address (optional).
        country (CharField): The country for shipping.
        city (CharField): The city for shipping.
        postal_code (CharField): The postal/ZIP code for the shipping address.

    Meta:
        verbose_name (str): A human-readable name for the model (singular).
        verbose_name_plural (str): A human-readable name for the model (plural).
    """
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, null=False, blank=False,related_name="shipping_address")
    address_line1 = models.CharField(max_length=200, null=True, blank=True)
    address_line2 = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=50, null=True, blank=True)
    updated_by = models.JSONField(blank=True, null=True)

    class Meta:
        verbose_name = "Order Shipping Address"
        verbose_name_plural = "Order Shipping Addresses"

    def __str__(self):
        return str(self.pk)


class OrderPayment(models.Model):
    """
    Represents the payment details for an order.

    Attributes:
        order_id (ForeignKey): A reference to the related order.
        payment_mode (CharField): The mode of payment (e.g., credit card, wallet).
        payment_status (CharField): The current status of the payment (e.g., pending, success).
        payment_date (DateTimeField): The timestamp when the payment was made.
        payment_amount (DecimalField): The amount paid for the order.
        payment_reference (CharField): A unique reference for the payment transaction.
        created_at (DateTimeField): The timestamp when the record was created.
        updated_at (DateTimeField): The timestamp when the record was last updated.

    Meta:
        verbose_name (str): A human-readable name for the model (singular).
        verbose_name_plural (str): A human-readable name for the model (plural).
    """
    PAYMENT_MODE_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('net_banking', 'Net Banking'),
        ('wallet', 'Wallet'),
        ('bkash', 'bKash'),
        ('rocket', 'Rocket'),
        ('nagad', 'Nagad'),
        ('cash_on_delivery', 'Cash On Delivery'),
    ]
    
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]
    
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, null=False, blank=False,related_name="payment_details")
    coupon_applied = models.ForeignKey(Coupon,on_delete=models.CASCADE,related_name='coupon',null=True,blank=True)
    payment_mode = models.CharField(max_length=50, choices=PAYMENT_MODE_CHOICES, null=False, blank=False)
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS, default='pending', null=False, blank=False)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    payment_reference = models.CharField(max_length=100, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.JSONField(blank=True, null=True)

    class Meta:
        verbose_name = "Order Payment"
        verbose_name_plural = "Order Payments"

    def __str__(self):
        return str(self.pk)


class Cart(models.Model):
    """
    Stores customer cart data for managing items before order placement.

    Attributes:
        device_ip (GenericIPAddressField): The IP address of the customer's device for tracking guest users.
        customer_id (ForeignKey): A reference to the logged-in customer (if available).
        cart_total_amount (DecimalField): The total cost of items in the cart.
        cart_checkout_status (BooleanField): Indicates if the cart has been checked out.
        created_at (DateTimeField): The timestamp when the cart was created.
        updated_at (DateTimeField): The timestamp when the cart was last updated.

    Meta:
        verbose_name (str): A human-readable name for the model (singular).
        verbose_name_plural (str): A human-readable name for the model (plural).
    """
    device_ip = models.GenericIPAddressField(verbose_name="Device IP",null=True,blank=True) #if the user is not loggedin, we are going to use device ip to track carts
    customer_id = models.ForeignKey(Accounts, on_delete=models.CASCADE, related_name="Cart",null=True,blank=True) #If the user is logged in, we are going to user customer id to track carts
    cart_total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cart Total Amount",default=0,null=True,blank=True)
    cart_checkout_status = models.BooleanField(default=False, verbose_name="Cart Checkout Status")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Customer Cart"
        verbose_name_plural = "Customer Carts"

    def __str__(self):
        return str(self.pk)


class CartItems(models.Model):
    """
    Represents individual items in a customer's cart.

    Attributes:
        cart_id (ForeignKey): A reference to the related cart.
        product_sku (ForeignKey): A reference to the product SKU added to the cart.
        quantity (PositiveIntegerField): The quantity of the product in the cart.
        created_at (DateTimeField): The timestamp when the record was created.
        updated_at (DateTimeField): The timestamp when the record was last updated.
    """
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE,null=False,blank=False)
    product_sku = models.ForeignKey(Product_SKU, on_delete=models.CASCADE,null=False,blank=False)
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity",null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return str(self.pk)

class CancelOrderRequest(models.Model):

    order_id = models.ForeignKey(Order,on_delete=models.CASCADE, null=False, blank=False,related_name="cancel_order")
    cancellation_reason = models.TextField(null=False,blank=False)
    cancellation_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    updated_by = models.JSONField(blank=True, null=True)

    class Meta:
        verbose_name = "Cancel Order"

    def __str__(self):
        return f"Order-ID:{self.order_id.order_id} - Reason:{self.cancellation_reason}, Status - {self.cancellation_status}"
    


