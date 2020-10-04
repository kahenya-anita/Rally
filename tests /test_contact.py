import unittest
from app.models import Contact
from app import db

class ContactModelTest(unittest.TestCase):
    def setUp(self):
        self.new_contact = Contact(name='name',email='email@ms.com', title='title', message='message')        

    def tearDown(self):
        Contact.query.delete()        

    def test_check_instance_variables(self):
        self.assertEquals(self.new_contact.name,'name')
        self.assertEquals(self.new_contact.email,'email@ms.com') 
        self.assertEquals(self.new_contact.title,'title')
        self.assertEquals(self.new_contact.message,'message')       
        
    def test_save_contact(self):
        self.new_contact.save_contact()
        self.assertTrue(len(Contact.query.all())>0)