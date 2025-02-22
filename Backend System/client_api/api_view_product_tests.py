from django.test import TestCase
from django.contrib.auth import get_user_model
from products.models import *
from orders.models import *
import json
from django.utils import timezone
from customer.models import *
import datetime
from rest_framework_simplejwt.tokens import AccessToken
from products.models import *


now = timezone.now()
User = get_user_model()

class ProductAPITests(TestCase):

    def setUp(self):
        now = timezone.now()
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
        self.product_sku3 = Product_SKU.objects.create(product_id=self.product2,product_color="silver",product_price=50,product_stock=50,created_at=now)

        self.product_sku1.product_flavours.set([self.product_flavour1])
        self.product_sku2.product_flavours.set([self.product_flavour2])
        self.product_sku3.product_flavours.set([self.product_flavour1,self.product_flavour2])

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

    def get_auth_header(self, user):
        token = AccessToken.for_user(user)
        return {'HTTP_AUTHORIZATION': f'Bearer {token}'}
    
    def test_fetch_product(self):

        #gll product search
        # data = {
        #     'search':'40'
        # }
        # response = self.client.get('/client_api/fetch/fetch_product_with_search/',data=data,format='json')
        # print(response.data)

        #with brand
        # data={
        #     'brand_name':'Dove'
        # }
        # response = self.client.get('/client_api/fetch/fetch_product_with_brand/',data=data,format='json')
        # print(response.data)

        #with category
        # data={
        #     'category_name':'Skincare'
        # }
        # response = self.client.get('/client_api/fetch/fetch_product_with_category/',data=data,format='json')
        # print(response.data)

        #with sub_category
        # data={
        #     'sub_category_name':'Cleansers'
        # }
        # response = self.client.get('/client_api/fetch/fetch_product_with_sub_category/',data=data,format='json')
        # print(response.data)

        #with price

        data={
            'min_price':'40',
            'max_price':'50'
        }
        response = self.client.get('/client_api/fetch/fetch_product_with_price/',data=data,format='json')
        # print(response.data)

    def test_fetch_brand(self):

        data={
            'brand_name':'Dove'
        }
        response = self.client.get('/client_api/fetch/fetch_brands/',data=data,format='json')
        print(response.data)
