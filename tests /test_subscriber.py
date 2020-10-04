import unittest
from app.models import Subscriber
from app import db

class SubscriberModelTest(unittest.TestCase):
    def setUp(self):
        self.new_subscriber = Subscriber(email='email@ms.com')
        

    def tearDown(self):
        Subscriber.query.delete()        

    def test_check_instance_variables(self):
        self.assertEquals(self.new_subscriber.email,'email@ms.com')        
        
    def test_save_subscriber(self):
        self.new_subscriber.save_subscriber()
        self.assertTrue(len(Subscriber.query.all())>0)