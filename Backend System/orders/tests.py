from django.test import TestCase,RequestFactory
from django.contrib.auth import get_user_model
from .models import *
from .order_management import OrderManagement
from .models import Accounts
from decimal import Decimal
import datetime
from products.models import *

User = get_user_model()

class OrderTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user1 = User.objects.create_user(
            email='user1@test.com',
            username='user1',
            password='testpass123'
        )

        self.delivery_time1 = DeliveryTime.objects.create(
            delivery_name= "Inside dhaka",
            estimated_delivery_time = "7 days"
        )
        self.delivery_time2 = DeliveryTime.objects.create(
            delivery_name= "Outside dhaka",
            estimated_delivery_time = "10 days"
        )
        self.delivery_time3 = DeliveryTime.objects.create(
            delivery_name= "Internation",
            estimated_delivery_time = "1 months"
        )

        self.customer1 = Accounts.objects.create(username="customer1", email="customer1@example.com")
        self.customer2 = Accounts.objects.create(username="customer2", email="customer2@example.com")
        self.customer3 = Accounts.objects.create(username="customer3", email="customer3@example.com")
        

        # Create product SKUs
        now = timezone.now()
        # Create categories
        self.category_skincare = Product_Category.objects.create(category_name="Skincare", description="Products for skincare", created_at=now)
        self.category_makeup = Product_Category.objects.create(category_name="Makeup", description="Products for makeup", created_at=now)
        self.category_haircare = Product_Category.objects.create(category_name="Haircare", description="Products for haircare", created_at=now)
        self.category_fragrance = Product_Category.objects.create(category_name="Fragrance", description="Products for fragrance", created_at=now)
        self.category_fragrance2 = Product_Category.objects.create(category_name="Fragrance2", description="Products for fragrance2", created_at=now)
        
        # Create sub-categories
        self.sub_category1 = Product_Sub_Category.objects.create(sub_category_name="Moisturizers", description="Products to moisturize skin", created_at=now)
        self.sub_category2 = Product_Sub_Category.objects.create(sub_category_name="Cleansers", description="Products to cleanse skin", created_at=now)
        self.sub_category3 = Product_Sub_Category.objects.create(sub_category_name="Shampoos", description="Products to clean hair", created_at=now)
        self.sub_category4 = Product_Sub_Category.objects.create(sub_category_name="Perfumes", description="Fragrance products", created_at=now)
        self.sub_category5 = Product_Sub_Category.objects.create(sub_category_name="Lipsticks", description="Lip makeup products", created_at=now)
        self.sub_category6 = Product_Sub_Category.objects.create(sub_category_name="Lipsticks6", description="Lip makeup products6", created_at=now)
        
        # Assign sub-categories to categories
        self.sub_category1.category_id.set([self.category_skincare])
        self.sub_category2.category_id.set([self.category_skincare])
        self.sub_category3.category_id.set([self.category_haircare])
        self.sub_category4.category_id.set([self.category_fragrance])
        self.sub_category5.category_id.set([self.category_makeup])
        self.sub_category6.category_id.set([self.category_fragrance2])

        #creating product brand
        #self.brand_logo = TestManageProducts.generate_test_image('white',1)
        self.brand1 = Product_Brands.objects.create(brand_name="Loreal", brand_country="USA",brand_description="Loreal Paris",
                                                    brand_established_year= 1909,is_own_brand=False,created_at=now)
        self.brand2 = Product_Brands.objects.create(brand_name="Dove", brand_country="USA",brand_description="Loreal Paris",
                                                    brand_established_year= 2000,is_own_brand=True,created_at=now)
        self.brand3 = Product_Brands.objects.create(brand_name="Dove11", brand_country="USA11",brand_description="Loreal Paris111",
                                                    brand_established_year= 2005,is_own_brand=True,created_at=now)
    
        #creating product flavours
        self.product_flavour1 = Product_Flavours.objects.create(product_flavour_name="Vanilla", created_at=now)
        self.product_flavour2 = Product_Flavours.objects.create(product_flavour_name="Strawberry", created_at=now)

        #creating products
        self.product1 = Product.objects.create(product_name="Loreal Moisturizer", product_brand=self.brand1,
                                       product_description="A moisturizer by Loreal", product_summary="Hydrating moisturizer",
                                       product_ingredients="Water, Glycerin", product_usage_direction="Apply daily", created_at=now)
        self.product1.product_category.set([self.category_skincare])
        self.product1.product_sub_category.set([self.sub_category1,self.sub_category2])

        self.product2 = Product.objects.create(product_name="Dove Cleanser", product_brand=self.brand2,
                                            product_description="A cleanser by Dove", product_summary="Gentle cleanser",
                                            product_ingredients="Water, Sodium Laureth Sulfate", product_usage_direction="Use twice daily", created_at=now)
        self.product2.product_category.set([self.category_skincare])
        self.product2.product_sub_category.set([self.sub_category2])
        

        self.product3 = Product.objects.create(product_name="Loreal Shampoo", product_brand=self.brand1,
                                            product_description="A shampoo by Loreal", product_summary="Cleansing shampoo",
                                            product_ingredients="Water, Sodium Laureth Sulfate", product_usage_direction="Use as needed", created_at=now)
        self.product3.product_category.set([self.category_haircare])
        self.product3.product_sub_category.set([self.sub_category3])

        self.product4 = Product.objects.create(product_name="Dove Perfume", product_brand=self.brand2,
                                            product_description="A perfume by Dove", product_summary="Long-lasting fragrance",
                                            product_ingredients="Alcohol, Fragrance", product_usage_direction="Spray on pulse points", created_at=now)
        self.product4.product_category.set([self.category_fragrance])
        self.product4.product_sub_category.set([self.sub_category4])
    

        self.product5 = Product.objects.create(product_name="Loreal Lipstick", product_brand=self.brand1,
                                            product_description="A lipstick by Loreal", product_summary="Matte lipstick",
                                            product_ingredients="Wax, Pigment", product_usage_direction="Apply on lips", created_at=now)
        self.product5.product_category.set([self.category_makeup])
        self.product5.product_sub_category.set([self.sub_category5])

        self.product6 = Product.objects.create(product_name="Loreal Lipstick52", product_brand=self.brand3,
                                            product_description="A lipstick by Lorea5252l", product_summary="Matte lipstick25252",
                                            product_ingredients="Wax, Pigment25252", product_usage_direction="Apply on lips2525", created_at=now)
        self.product6.product_category.set([self.category_fragrance2])
        self.product6.product_sub_category.set([self.sub_category6])
        

        #creating product sku
        self.product_sku1 = Product_SKU.objects.create(product_id=self.product1,product_color="white",product_price=25.3,product_stock=100,created_at=now)
        self.product_sku2 = Product_SKU.objects.create(product_id=self.product1,product_color="silver",product_price=50,product_stock=50,created_at=now)

        self.product_sku1.product_flavours.set([self.product_flavour1])
        self.product_sku2.product_flavours.set([self.product_flavour2])

        self.active_discount = Product_Discount.objects.create(
            discount_name="Active Discount",
            discount_amount=10.00,
            start_date=now - datetime.timedelta(days=1),  # Started yesterday
            end_date=now + datetime.timedelta(days=10),    # Ends in 10 days
            is_active=False,
            product_id_pk=1
        )
        self.active_discount.save()
        self.active_discount.product_id.add(self.product1)
        self.active_discount.save()

        # Inactive discount (end date in the past)
        self.inactive_discount = Product_Discount.objects.create(
            discount_name="Inactive Discount",
            discount_amount=5.00,
            start_date=now - datetime.timedelta(days=10),  # Started 10 days ago
            end_date=now - datetime.timedelta(days=1),      # Ended yesterday
            product_id_pk=2
        )
        self.inactive_discount.save()
        self.inactive_discount.product_id.add(self.product2)
        self.inactive_discount.save()

        # Inactive discount (start date in the future)
        self.future_discount = Product_Discount.objects.create(
            discount_name="Future Discount",
            discount_amount=15.00,
            start_date=now + datetime.timedelta(days=1),  # Starts tomorrow
            end_date=now + datetime.timedelta(days=10),    # Ends in 10 days
            brand_id_pk = 1
        )
        self.future_discount.save()
        self.future_discount.product_id.add(self.product3)
        self.future_discount.save()

        # Create test orders
        self.order1 = Order.objects.create(
            order_id="ORD001",
            customer_id=self.customer1,
            delivery_time=self.delivery_time1,
            total_amount=Decimal("90.50"),
            order_status="pending",
        )

        self.order2 = Order.objects.create(
            order_id="ORD002",
            customer_id=self.customer2,
            delivery_time=self.delivery_time2,
            total_amount=Decimal("150.00"),
            order_status="shipped",
        )

        self.order3 = Order.objects.create(
            order_id="ORD003",
            customer_id=self.customer3,
            delivery_time=self.delivery_time1,
            total_amount=Decimal("50.75"),
            order_status="delivered",
        )

        # Create order details
        self.order_details1 = OrderDetails.objects.create(
            order_id=self.order1,
            product_sku=self.product_sku1,
            quantity=2,
            units=1,
            subtotal=Decimal("60.00")
        )

        self.order_details2 = OrderDetails.objects.create(
            order_id=self.order2,
            product_sku=self.product_sku2,
            quantity=3,
            units=1,
            subtotal=Decimal("136.50")
        )

        self.order_details3 = OrderDetails.objects.create(
            order_id=self.order3,
            product_sku=self.product_sku2,
            quantity=1,
            units=1,
            subtotal=Decimal("20.75")
        )

        # Create shipping addresses
        self.shipping1 = OrderShippingAddress.objects.create(
            order_id=self.order1,
            address_line1="123 Main St",
            city="New York",
            country="USA",
            postal_code="10001"
        )

        self.shipping2 = OrderShippingAddress.objects.create(
            order_id=self.order2,
            address_line1="456 Elm St",
            city="Los Angeles",
            country="USA",
            postal_code="90001"
        )

        self.shipping3 = OrderShippingAddress.objects.create(
            order_id=self.order3,
            address_line1="789 Oak St",
            city="Chicago",
            country="USA",
            postal_code="60601"
        )

        # Create coupons
        self.coupon1 = Coupon.objects.create(
            coupon_code = 'UNIQUE1',
            discount_type = Coupon.DISCOUNT_TYPE_CHOICES[0][0],#percentage
            discount_percentage=30,
            maximum_discount_amount=100,
            start_date = now,
            end_date = now + datetime.timedelta(days=10),
            customer_id = self.customer1,
            created_at = now

        )

        self.coupon2 = Coupon.objects.create(
            coupon_code = 'UNIQUE2',
            discount_type = Coupon.DISCOUNT_TYPE_CHOICES[1][1],#fixed
            discount_amount=50,
            usage_limit=1,
            maximum_discount_amount=100,
            start_date = now + datetime.timedelta(days=-5),
            end_date = now + datetime.timedelta(days=20),
            customer_id = self.customer2,
            created_at = now

        )

        # Create payments
        self.payment1 = OrderPayment.objects.create(
            order_id=self.order1,
            coupon_applied=self.coupon1,
            payment_mode="credit_card",
            payment_status="success",
            payment_amount=Decimal("81.45"),
            payment_reference="PAY123"
        )

        self.payment2 = OrderPayment.objects.create(
            order_id=self.order2,
            coupon_applied=self.coupon2,
            payment_mode="paypal",
            payment_status="success",
            payment_amount=Decimal("142.50"),
            payment_reference="PAY456"
        )

        self.payment3 = OrderPayment.objects.create(
            order_id=self.order3,
            coupon_applied=None,  # No coupon applied
            payment_mode="debit_card",
            payment_status="pending",
            payment_amount=Decimal("50.75"),
            payment_reference="PAY789"
        )

        self.cancelorder1= CancelOrderRequest.objects.create(
            order_id = self.order1,
            cancellation_reason = "yyy"
        )

    def _create_mock_dev_user(self):
        """ Helper method to create a mock user """
        return Accounts.objects.create(
            email='user@example.com',
            username='user',
            is_superuser = True,
            password='1234',
        )
    
    def test_fetch_delivery_time(self):

        request = self.factory.get('/delivery/fetch/')
        request.user = self._create_mock_dev_user()
        success,message = OrderManagement.fetch_delivery_time(delivery_pk=self.delivery_time1.pk)
        self.assertTrue(success,"Fetched")
        self.assertEqual(message,"Fetched Successfully")

    def test_create_delivery_time(self):

        request = self.factory.get('/delivery/fetch/')
        request.user = self._create_mock_dev_user()
        success,message = OrderManagement.create_delivery_time(request,"Inside dhaka","5 days")
        self.assertFalse(success,"Not created")
        self.assertEqual(message, "Delivery Time with this name already exists")

        success,message = OrderManagement.create_delivery_time(request,"Outside omar","pp")
        self.assertTrue(success,"Created")

    def test_update_delivery_time(self):

        request = self.factory.get('/delivery/fetch/')
        request.user = self._create_mock_dev_user()
        success,message = OrderManagement.update_delivery_time(request,self.delivery_time3.pk,"Indianaa","opop")
        self.assertTrue(success,"Updated")

    def test_delete_delivery_time(self):

        request = self.factory.get('/delivery/fetch/')
        request.user = self._create_mock_dev_user()
        success,message = OrderManagement.delete_delivery_time(request,self.delivery_time2.pk)
        self.assertTrue(success,"Deleted")

    #order test
    def test_fetch_order_details(self):

        request = self.factory.get('/order/fetch/')
        request.user = self._create_mock_dev_user()
        success,message = OrderManagement.fetch_orders_details(order_id='ORD001')
        self.assertTrue(success,"Fetched successfully")
        self.assertEqual(message,"Order Fetched Successfully")
        
        #username
        success,message = OrderManagement.fetch_orders_details(user_name=self.customer2.username)
        self.assertTrue(success,"Fetched successfully")
        
        #all
        success,message = OrderManagement.fetch_orders_details()
        self.assertTrue(success,"Fetched successfully")

    def test_fetch_cancellation_reason(self):

        request = self.factory.get('/order/fetch/')
        request.user = self._create_mock_dev_user()
        success,message = OrderManagement.fetch_order_cancellation_requests(order_cancellation_request_pk=self.cancelorder1.pk)
        print(success)

    def test_order_cancellation_request(self):

        request = self.factory.get('/order/fetch/')
        request.user = self._create_mock_dev_user()
        success,message = OrderManagement.order_cancellation_request(request,self.cancelorder1.pk,True)
        
    