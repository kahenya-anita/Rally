import unittest
from app.models import Post,Comment
from app import db

class PostModelTest(unittest.TestCase):
    def setUp(self):
        self.this_post = Post(title= 'title', text='text',  post_pic_path='postpicpath')        

    def tearDown(self):
        Post.query.delete()
        Comment.query.delete()

    def test_check_instance_variables(self):
        self.assertEquals(self.this_post.title,'title')
        self.assertEquals(self.this_post.content,'content')
        self.assertEquals(self.this_post.post_pic_path,'postpicpath')              

    def test_save_post(self):
        self.this_post.save_post()
        self.assertTrue(len(Post.query.all())>0)