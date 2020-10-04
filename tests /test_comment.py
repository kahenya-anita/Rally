import unittest
from app.models import Post,Comment
from app import db

class CommentModelTest(unittest.TestCase):
    def setUp(self):
        self.new_post = Post(title= 'title', text='text', post_pic_path='postpicpath')
        self.new_comment = Comment(comment_text='commenttext', post=self.new_post)

    def tearDown(self):
        Post.query.delete()
        Comment.query.delete()

    def test_check_instance_variables(self):
        self.assertEquals(self.new_comment.comment_text,'commenttext')        
        self.assertEquals(self.new_comment.post,self.new_post)

    def test_save_comment(self):
        self.new_comment.save_comment()
        self.assertTrue(len(Comment.query.all())>0)