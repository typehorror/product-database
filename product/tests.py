"""
rest interface testing
"""
from django.utils.functional import curry
from django.test import TestCase

from binascii import b2a_base64

from models import Product, Category

class BasicTest(TestCase):

    fixtures = ['test.json',]
        
    def setUp(self):
        self.client.put = curry(self.client.post, REQUEST_METHOD='PUT')
        self.client.delete = curry(self.client.get, REQUEST_METHOD='DELETE')
        self.headers = {'HTTP_AUTHORIZATION': 'Basic %s' % b2a_base64('rest:rest')[:-1]}
        self.adminheaders = {'HTTP_AUTHORIZATION': 'Basic %s' % b2a_base64('restadmin:restadmin')[:-1]}

    def test_security_on_post(self):
        url = '/product/'
        response = self.client.post(url,{'description':'my new description'})
        self.failUnlessEqual(response.status_code, 401)

    def test_security_on_put(self):
        # test the update url
        url = '/product/FCFQ18W827/'
        response = self.client.put(url,{'description':'my new description'})
        self.failUnlessEqual(response.status_code, 401)

    def test_security_on_delete(self):
        # test the delete product url
        url = '/product/FCFQ18W827/'
        response = self.client.delete(url)
        self.failUnlessEqual(response.status_code, 401)

    def test_security_on_get(self):
        # test the listing url

        url = '/product/'
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 401)
        # test the product detail url
        url = '/product/FCFQ18W827/'
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 401)

    def test_create_product(self):
        url = '/product/'
        new_product = { 
            'item_number': '3H78GH55',
            'title': 'new product',
            'description': 'this is a new product',
            'category': 'qwerty',
        }

        # should fail because of the user permissions
        response = self.client.post(url, new_product, **self.headers)
        self.failUnlessEqual(response.status_code, 401)

        response = self.client.post(url, new_product, **self.adminheaders)
        # Request should be validated by a 200
        self.failUnlessEqual(response.status_code, 200)
        # The category is supposed to be auto created
        category = Category.objects.get(ref=new_product['category'])
        products = category.products.all()
        # category should be link to a single product
        self.assertEqual(len(products), 1)
        product = products[0]
        # Check object consistency
        self.assertEqual(product.title, new_product['title'])
        self.assertEqual(product.description, new_product['description'])
        self.assertEqual(product.category, category)

    def test_get_object(self):
        product = Product.objects.all()[0]
        url = '/product/%s/' % product.item_number

        response = self.client.get(url, **self.headers)
        # Request should be validated by a 200
        self.failUnlessEqual(response.status_code, 200)

    def test_put_object(self):
        product = Product.objects.all()[0]
        url = '/product/%s/' % product.item_number
        # first test we update description
        values = {'description': 'New description'}

        # should fail because of the user permissions
        response = self.client.put(url, values, **self.headers)
        self.failUnlessEqual(response.status_code, 401)

        response = self.client.put(url, values, **self.adminheaders)
        # Request should be validated by a 200
        self.failUnlessEqual(response.status_code, 200)
        # Check object consistency
        updated_product = Product.objects.get(pk=product.pk)
        self.assertEqual(product.title, updated_product.title)
        self.assertEqual(product.category, updated_product.category)
        self.assertEqual(values['description'], updated_product.description)
        
        # second test: we update category which is a related object
        values = {'category':'23545747'}
        response = self.client.put(url, values, **self.adminheaders)
        # Request should be validated by a 200
        self.failUnlessEqual(response.status_code, 200)
        # Check object consistency
        product = updated_product
        category = Category.objects.get(ref=values['category'])
        updated_products = category.products.all()
        self.assertEqual(len(updated_products), 1)
        updated_product = updated_products[0]
        self.assertEqual(product.title, updated_product.title)
        self.assertEqual(category, updated_product.category)
        self.assertEqual(product.description, updated_product.description)

    def test_put_wrong_property_name(self):
        product = Product.objects.all()[0]
        url = '/product/%s/' % product.item_number
        # first test we update description
        values = {'wrong_1245': 'Wrong property name'}

        # should fail because of the user permissions
        response = self.client.put(url, values, **self.headers)
        self.failUnlessEqual(response.status_code, 401)

        response = self.client.put(url, values, **self.adminheaders)
        self.failUnlessEqual(response.status_code, 404)
        

    def test_delete_object(self):
        # Make sure that the object exists
        product_item_number = 'DLB09PRO'
        product = Product.objects.get(item_number=product_item_number)
        url = '/product/%s/' % product_item_number
        
        # should fail because of the user permissions
        response = self.client.delete(url, **self.headers)
        self.failUnlessEqual(response.status_code, 401)

        response = self.client.delete(url, **self.adminheaders)
        # Request should be validated by a 200
        self.failUnlessEqual(response.status_code, 200)
        self.assertRaises(Product.DoesNotExist, Product.objects.get,item_number=product_item_number) 
        # make sure that the category hasn't been deleted
        Category.objects.get(pk=product.category_id)

    def test_basic_header_auth(self):
        url = '/product/'

        # First wrong password should fail 
        headers = { 'HTTP_AUTHORIZATION': 'Basic %s' % b2a_base64('rest:wrong_password')[:-1]}
        response = self.client.get(url,**headers)
        self.failUnlessEqual(response.status_code, 401)
    
        # Right password should succeed
        response = self.client.get(url,**self.headers)
        self.failUnlessEqual(response.status_code, 200)

