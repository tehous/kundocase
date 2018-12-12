from django.test import TestCase
from kundocase.forum.forms import TopicForm,PostForm
from django.forms.models import ModelFormMetaclass as formClass

class TestForms(TestCase):
    def testTopicForm(self):
        self.assertEqual(list(TopicForm().fields.keys()),['content'])
        self.assertEqual(type(TopicForm),formClass)
    
    def testPostForm(self):
        self.assertEqual(list(PostForm().fields.keys()),['content', 'user_name', 'user_email'])
        self.assertEqual(type(PostForm),formClass)

