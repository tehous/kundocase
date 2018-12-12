from django.test import TestCase
from kundocase.forum.models import Topic, PostModel

class BaseSetup(object):
    def setUp(self):
        self.topic=Topic(content="not too long")
        self.topic.save()
        self.spam=Topic(content="Spam!"*50)
        self.spam.save()


class TopicTests(BaseSetup,TestCase):
    def test_marked_as_spam(self):
        self.assertFalse(self.topic.is_spam)
        self.assertTrue(self.spam.is_spam)
    
    def test_spam_for_staff(self):
        self.assertIn(self.spam, Topic.adminmanager.all())
        self.assertNotIn(self.spam, Topic.objects.all())

class PostModelTests(BaseSetup,TestCase):
    def setUp(self):
        super(PostModelTests,self).setUp()
        self.t1=self.topic.last_post
        self.post1=PostModel(
                             topic=self.topic,
                             user_email="foo@bar.com",
                             user_name="foo bar",
                             content="content"
                            )
        
        self.post2=PostModel(
                             topic=self.spam,
                             user_email="foo@bar.com",
                             user_name="foo bar",
                             content="content"
                            )
        
        self.post3=PostModel(
                             topic=self.topic,
                             user_email="foo@bar.com",
                             user_name="foo bar",
                             content="spam!"*50
                            )
        self.post1.save()
        self.post2.save()
        self.post3.save()

    def test_marked_as_spam(self):
        self.assertFalse(self.post1.is_spam)
        self.assertTrue(self.post2.is_spam)
        self.assertTrue(self.post3.is_spam)

    def test_spam_op_and_spam_topic(self):
        self.post3.original_post=True
        self.post3.save()
        self.assertTrue(self.topic.is_spam)
    
    def test_updates_topic_last_post(self):
        self.assertEqual(self.topic.last_post,self.post3.created)
        self.assertNotEqual(self.t1, self.topic.last_post)