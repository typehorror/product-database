"""
stock check logging interface testing
"""
from datetime import datetime
from binascii import b2a_base64


from django.test.client import Client
from django.test import TestCase
from django.core.urlresolvers import reverse


from product.models import Product
from models import StockCheck

class BasicTest(TestCase):

    fixtures = ['categories.json',
                'groups.json',
                'permissions.json',
                'products.json',
                'users.json',
                'inventories.json',
                'warehouses.json',
                ]
        
    def setUp(self):
        self.client = Client()

    @property
    def rest_headers(self):
        self.username = 'rest'
        self.password = 'rest'
        auth = '%s:%s' % (self.username, self.password)
        return {'HTTP_AUTHORIZATION': 'Basic %s' % b2a_base64(auth)[:-1]}

    def connect_client(self):
        self.username = 'admin'
        self.password = 'admin'
        self.client.post('/login/', {'username': self.username, 'password': self.password})


    def test_access_logged_on_quantity_checked_web(self):
        """
        test that the quantity check is logged when using Web interface
        """
        stock_check_count = StockCheck.objects.count()
        quantity_requested = 5
        product = Product.objects.all()[0]
        before_access = datetime.now()
        url = reverse('ajax_stock_available', args=[product.item_number])
        self.connect_client()
        self.client.post(url, {'quantity': quantity_requested})
        after_access = datetime.now()
        stock_check_list = StockCheck.objects.filter(stock_query=quantity_requested,
                                                     creation_date__lte = after_access,
                                                     creation_date__gte = before_access)        

        # we should get 1 new record
        self.assertEqual(len(stock_check_list), 1L)
        self.assertEqual(StockCheck.objects.count(), stock_check_count+1)
        
        # the user should be logged
        stock_check = stock_check_list[0]
        self.assertEqual(stock_check.user.username, self.username)

        # the ip_address should be the loopback
        self.assertEqual(stock_check.ip_address, '127.0.0.1')

        # the interface should be web
        self.assertEqual(stock_check.interface, 'web')
        
    def test_access_logged_on_quantity_checked_rest(self):
        """
        test that the quantity check is logged when using REST API
        """
        stock_check_count = StockCheck.objects.count()
        quantity_requested = 15
        product = Product.objects.all()[0]
        before_access = datetime.now()
        url = '/product/xml/%s/%d/' % (product.item_number, quantity_requested)
        self.client.get(url, **self.rest_headers)
        after_access = datetime.now()
        stock_check_list = StockCheck.objects.filter(stock_query=quantity_requested,
                                                     creation_date__lte = after_access,
                                                     creation_date__gte = before_access)        

        # we should get 1 new record
        self.assertEqual(len(stock_check_list), 1L)
        self.assertEqual(StockCheck.objects.count(), stock_check_count+1)
        
        # the user should be logged
        stock_check = stock_check_list[0]
        self.assertEqual(stock_check.user.username, self.username)

        # the ip_address should be the loopback
        self.assertEqual(stock_check.ip_address, '127.0.0.1')

        # the interface should be rest
        self.assertEqual(stock_check.interface, 'rest')
