from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from products.models import *
from products import product_serializers
from business_admin.models import *
from django.db.models import Q

# Create your tests here.
class ProductCategoryAPITestCases(APITestCase):
    
    def setUp(self):
        self.now = timezone.now()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.product_category1 = Product_Category.objects.create(category_name="Skincare", description="Products for skincare", created_at=self.now)
        self.product_category2= Product_Category.objects.create(category_name="Makeup", description="Products for makeup", created_at=self.now)
        self.product_sub_category1 = Product_Sub_Category.objects.create(sub_category_name="Moisturizers", description="Products to moisturize skin", created_at=self.now)
        self.product_sub_category2= Product_Sub_Category.objects.create(sub_category_name="Cleansers", description="Products to cleanse skin", created_at=self.now)

        self.product_sub_category1.category_id.set([self.product_category1,self.product_category2])
        self.product_sub_category2.category_id.set([self.product_category2])

        self.adminposition1 = AdminPositions.objects.create(name="Owner",description="Ownerrr")
        self.product_brand1 = Product_Brands.objects.create(brand_name="Loreal", brand_country="USA",brand_description="Loreal Paris",
                                                    brand_established_year= 1909,is_own_brand=False,created_at=self.now)
        self.product_brand2 = Product_Brands.objects.create(brand_name="Dove", brand_country="USA",brand_description="Loreal Paris",
                                                    brand_established_year= 2000,is_own_brand=True,created_at=self.now)
        
        self.product_flavour1 = Product_Flavours.objects.create(product_flavour_name="Vanilla", created_at=self.now)
        self.product_flavour2 = Product_Flavours.objects.create(product_flavour_name="Strawberry", created_at=self.now)

        self.product1 = Product.objects.create(product_name="Dove Cleanser", product_brand=self.product_brand2,
                                            product_description="A cleanser by Dove", product_summary="Gentle cleanser",
                                            product_ingredients="Water, Sodium Laureth Sulfate", product_usage_direction="Use twice daily", created_at=self.now)
        self.product1.product_category.set([self.product_category2])
        self.product1.product_sub_category.set([self.product_sub_category2])
        self.product1.product_flavours.set([self.product_flavour2])

        self.product2 = Product.objects.create(product_name="Dove85 Cleanser", product_brand=self.product_brand1,
                                            product_description="A cleanser by Dove", product_summary="Gentle cleanser",
                                            product_ingredients="Water, Sodium Laureth Sulfate", product_usage_direction="Use twice daily", created_at=self.now)
        self.product2.product_category.set([self.product_category1])
        self.product2.product_sub_category.set([self.product_sub_category1])
        self.product2.product_flavours.set([self.product_flavour1])


    def test_fetch_all_product_categories(self):
        """
        Test
        for fetching product categories
        """
        response = self.client.get('/server_api/product/categories/fetch_all/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data['product_category']),2)
        expected_data = Product_Category.objects.all()
        returned_data = response.data['product_category']
        expected_data_serialized = product_serializers.Product_Category_Serializer(expected_data, many=True).data
        self.assertEqual(returned_data, expected_data_serialized)

        #single
        response = self.client.get(f'/server_api/product/categories/fetch_all/?{self.product_category1.pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = Product_Category.objects.get(pk=self.product_category1.pk)
        returned_data = response.data['product_category'][0]
        expected_data_serialized = product_serializers.Product_Category_Serializer(expected_data, many=False).data
        self.assertEqual(returned_data, expected_data_serialized)


    def test_fetch_a_product_category(self):

        """
        Test
        for fetching a product category
        """
        response = self.client.get(f'/server_api/product/categories/{self.product_category1.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = Product_Category.objects.get(pk=self.product_category1.pk)
        returned_data = response.data['product_category']
        expected_data_serialized = product_serializers.Product_Category_Serializer(expected_data, many=False).data
        self.assertEqual(returned_data, expected_data_serialized)



    def test_create_product_categories(self):
        """
        Test
        for creating product categories also for duplicate as well
        """
        data = {"category_name": "Test Product", "description": "Test Description"}
        response = self.client.post('/server_api/product/categories/create/', data,format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'],"New Product category. Test Product successfully added!")

        response = self.client.post('/server_api/product/categories/create/', data,format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'],"Same type exists in Database!","Not Equal")

    def test_update_product_categories(self):
        """
        Test
        for updating product categories
        """
        
        data = {"category_name": "Glass Skincare", "description": "Products for glass skincare"}
        response = self.client.put(f'/server_api/product/categories/update/{self.product_category1.pk}/', data,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'],"Product Category updated successfully!")

    def test_delete_product_categories(self):
        """
        Test
        for deleting product categories
        """

        response = self.client.delete(f'/server_api/product/categories/delete/{self.product_category2.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data['message'],"Product Category deleted successfully!")
        self.assertFalse(Product_Category.objects.filter(pk=self.product_category2.pk).exists(),False)

        #deleting again
        response = self.client.delete(f'/server_api/product/categories/delete/{self.product_category2.pk}/')
        self.assertTrue(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'],"Product Category does not exist!")

    #test for product sub categories
    def test_fetch_all_product_sub_category_for_a_category(self):
        """
        Test
        for fetching product sub categories
        """

        response = self.client.get(f'/server_api/product/sub_categories/fetch_all_product_sub_categories_for_a_category/{self.product_category2.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data['product_sub_category']),2)
        expected_data = Product_Sub_Category.objects.filter(category_id = self.product_category2)
        returned_data = response.data['product_sub_category']
        expected_data_serialized = product_serializers.Product_Sub_Category_Serializer(expected_data, many=True).data
        self.assertEqual(returned_data, expected_data_serialized)

    def test_create_product_sub_category(self):
        """
        Test
        for creating product sub categories
        """
        data = {"sub_category_name": "Foundation", "description": "Foundation Description"}
        response = self.client.post(f'/server_api/product/sub_categories/create/{self.product_category2.pk}/',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'],"New Product sub-category, Foundation successfully added!","Success message is incorrect")
        
        #if duplicate
        response = self.client.post(f'/server_api/product/sub_categories/create/{self.product_category2.pk}/',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'],"Same type exists in Database!","Success message is incorrect")
   

    def test_update_product_sub_category(self):

        """
          Test
        for updating product sub categories
        """

        data = {"category_pk_list":[self.product_category1.pk],"sub_category_name": "Moisturizers lop", "description": "Moisturizers Description"}
        response = self.client.put(f'/server_api/product/sub_categories/update/{self.product_sub_category1.pk}/',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['message'],"Product Sub Category updated successfully!","Success message is incorrect")


    def test_delete_product_sub_category(self):
        """
          Test
        for deleting product sub categories
        """
        response = self.client.delete(f'/server_api/product/sub_categories/delete/{self.product_sub_category1.pk}/')
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data['message'],"Product Sub Category deleted successfully!","Success message is incorrect")

        #deleting again
        response = self.client.delete(f'/server_api/product/sub_categories/delete/{self.product_sub_category1.pk}/')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'],"Product Sub Category does not exist!","Success message is incorrect")

    #business_admin login in/signup
    def test_token_fetch(self):
        """
        Test for fetching token
        """

        data = {
            'username':self.user.username
        }
        response = self.client.post(f'/server_api/business_admin/fetch_token/',data,format='json')
        self.assertEqual(response.data['message'],"Token fetched successfully")
        self.assertIn('token', response.data) 

    def test_business_admin_signup(self):
        """
        Test for signing up business admin
        """
        data = {
            "admin_full_name": "John Doe",
            "admin_user_name": "johndoe",
            "password": "securepassword",
            "confirm_password": "securepassword",
            "admin_position_pk": self.adminposition1.pk,
            "admin_contact_no": "1234567890",
            "admin_email": "john.doe@example.com",
        }
        response = self.client.post(f'/server_api/business_admin/signup/',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'],"Business Admin created successfully. Redirecting to dashboard...","Success messsage is incorrect")
        self.assertEqual(response.data['redirect_url'],"/dashboard","Success messsage is incorrect")
        self.assertTrue(User.objects.filter(username="johndoe").exists())
        self.assertTrue(BusinessAdminUser.objects.filter(admin_full_name="John Doe").exists())

    def test_business_admin_log_in(self):
        """
        Test for loggin in 
        """
        data = {
            "username":"testuser",
            "password":"password"
        }
        response = self.client.post(f'/server_api/business_admin/login/',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['message'],"Logged In","Success message is incorrect")

        #incorrect data
        data = {
            "username":"testuser2",
            "password":"password22"
        }
        response = self.client.post(f'/server_api/business_admin/login/',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'],"Username or Password incorrect!","Success message is incorrect")

        #no data
        data ={
            "username":None,
            "password":None
        }
        response = self.client.post(f'/server_api/business_admin/login/',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'],"Username or Password must be provided!","Success message is incorrect")

    def test_logout_successful(self):
        """
        Test that a user can successfully log out and is redirected to the login page.
        """
        response = self.client.post(f'/server_api/business_admin/logout/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('redirect_url', response.data) 
        self.assertEqual(response.data['redirect_url'], '/server_api/business_admin/login/') 
        # Check that the token is deleted
        with self.assertRaises(Token.DoesNotExist):
            Token.objects.get(user=self.user)

    def test_logout_unauthenticated(self):
        """
        Test that an unauthenticated user cannot access the logout endpoint.
        """
        self.client.credentials()  
        response = self.client.post(f'/server_api/business_admin/logout/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data) 
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    #product brands
    def test_fetch_product_brand(self):
        """
        Test for creating product brand
        """
        #fetching all
        response = self.client.get(f'/server_api/product/product_brand/fetch_product_brands/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data['product_brands']),2)
        expected_data = Product_Brands.objects.all()
        returned_data = response.data['product_brands']
        expected_data_serialized = product_serializers.Product_Brands_Serializer(expected_data, many=True).data
        self.assertEqual(returned_data, expected_data_serialized)

        #fetching single
        response = self.client.get(f'/server_api/product/product_brand/fetch_product_brands/?pk={self.product_brand1.pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = Product_Brands.objects.get(pk=self.product_brand1.pk)
        returned_data = response.data['product_brands']
        expected_data_serialized = product_serializers.Product_Brands_Serializer(expected_data, many=False).data
        self.assertEqual(returned_data, expected_data_serialized)

        #fetching using name
        response = self.client.get(f'/server_api/product/product_brand/fetch_product_brands/?brand_name={self.product_brand1.brand_name}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = Product_Brands.objects.get(pk=self.product_brand1.pk)
        returned_data = response.data['product_brands']
        expected_data_serialized = product_serializers.Product_Brands_Serializer(expected_data, many=False).data
        self.assertEqual(returned_data, expected_data_serialized)

    def test_create_product_brand(self):
        """
        Test for creating product brand
        """
        data = {'brand_name':"simu",'brand_established_year':2008,'is_own_brand':True}
        response = self.client.post(f'/server_api/product/product_brand/create/',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'],"Brand created")

        #duplicate
        data = {'brand_name':"Loreal",'brand_established_year':2008,'is_own_brand':True}
        response = self.client.post(f'/server_api/product/product_brand/create/',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'],"Same brand exists in Database!")

    def test_update_product_brand(self):
        """
        Test for updating product brand
        """
        data = {'brand_name':self.product_brand1.brand_name,'brand_established_year':2010}
        response = self.client.put(f'/server_api/product/product_brand/update/{self.product_brand1.pk}',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'],"Brand updated")

        #same name
        data = {'brand_name':'Dove','brand_established_year':2010}
        response = self.client.put(f'/server_api/product/product_brand/update/{self.product_brand1.pk}',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'],"Same brand already exists!")

    def test_delete_product_brand(self):
        """
        Test for deleting product brand
        """
        response = self.client.delete(f'/server_api/product/product_brand/delete/{self.product_brand1.pk}') 
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data['message'],"Product brand deleted successfully!")

    #test product flavours
    def test_fetch_product_flavours(self):
        """
        Test to fetch product flavours
        """
        #all fetch
        response = self.client.get(f'/server_api/product/product_flavour/fetch_product_flavour/')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data['product_flavours_data']),2) 
        expected_data = Product_Flavours.objects.all()
        expected_data = product_serializers.Product_Flavour_Serializer(expected_data,many=True).data
        returned_data = response.data['product_flavours_data']
        self.assertEqual(returned_data,expected_data)

        #pk
        response = self.client.get(f'/server_api/product/product_flavour/fetch_product_flavour/?pk={self.product_flavour1.pk}')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),2) 
        expected_data = Product_Flavours.objects.get(pk=self.product_flavour1.pk)
        expected_data = product_serializers.Product_Flavour_Serializer(expected_data,many=False).data
        returned_data = response.data['product_flavours_data']
        self.assertEqual(returned_data,expected_data)

    def test_create_product_flavour(self):
        """
        Test for creating product flavour
        """
        data = {'product_flavour_name':"anana"}
        response = self.client.post(f'/server_api/product/product_flavour/create/',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'],"New Product flavour, anana successfully added!")

        #duplicate
        data = {'product_flavour_name':self.product_flavour2.product_flavour_name}
        response = self.client.post(f'/server_api/product/product_flavour/create/',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'],"Same flavour exists in Database!")

    def test_update_product_flavour(self):
        """
        test for updating product flavour
        """

        data = {'product_flavour_pk':self.product_flavour1.pk,'product_flavour_name':"sami"}
        response = self.client.put(f'/server_api/product/product_flavour/update/{self.product_flavour1.pk}',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['message'],"Product flavour updated successfully!")

    def test_delete_product_flavour(self):
        """
        test for deleting product flavour
        """
        response = self.client.delete(f'/server_api/product/product_flavour/delete/{self.product_flavour1.pk}')
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data['message'],"Product flavour deleted successfully!")

    #product tests
    def test_fetch_product(self):
        """
        test for fetching product
        """        
        #all
        response = self.client.get(f'/server_api/product/fetch_product/')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        existing_data = Product.objects.all()
        existing_data = product_serializers.Product_Serializer(existing_data,many=True).data
        returned_data = response.data['product_data']
        self.assertEqual(existing_data,returned_data)
        #using category list
        response = self.client.get(f'/server_api/product/fetch_product/?product_category_pk_list={[self.product_category1.pk,self.product_category2.pk]}')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        existing_data = Product.objects.filter(Q(product_category = self.product_category1) | Q(product_category = self.product_category2))
        existing_data = product_serializers.Product_Serializer(existing_data,many=True).data
        returned_data = response.data['product_data']
        self.assertEqual(existing_data,returned_data)

        #using sub category list
        response = self.client.get(f'/server_api/product/fetch_product/?product_sub_category_pk_list={[self.product_sub_category1.pk,self.product_sub_category2.pk]}')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        existing_data = Product.objects.filter(Q(product_sub_category = self.product_sub_category1.pk) | Q(product_sub_category = self.product_sub_category2))
        existing_data = product_serializers.Product_Serializer(existing_data,many=True).data
        returned_data = response.data['product_data']
        self.assertEqual(existing_data,returned_data)

    def test_create_product(self):
        """
        Test for creating product
        """
        
        data = {'product_name':"ooo",'product_category_pk_list':[self.product_category1.pk,self.product_category2.pk],
                'product_sub_category_pk_list' : [self.product_sub_category1.pk],'product_description':"pppp",
                'product_summary':"ppopop",'product_flavours_pk_list':[self.product_flavour1.pk,self.product_flavour2.pk],
                }
        response = self.client.post(f'/server_api/product/create/',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'],"Product, ooo created!")
        
        #duplicate
        data = {'product_name':"Dove Cleanser",'product_category_pk_list':[self.product_category1.pk,self.product_category2.pk],
                'product_sub_category_pk_list' : [self.product_sub_category1.pk],'product_description':"pppp",
                'product_summary':"ppopop",'product_flavours_pk_list':[self.product_flavour1.pk,self.product_flavour2.pk],
                }
        response = self.client.post(f'/server_api/product/create/',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'],"Same product already exists!")