from django.test import TestCase
from kundocase.forum.views import topicListview, get_topics, post_topic,api_new_topic_forms
from kundocase.forum.views import topicView, get_topic,post_post, api_post_form
from django.urls.base import reverse
from kundocase.forum.models import Topic, PostModel
import json


class TestTopics(TestCase):
    def setUp(self):
        self.validForm={
            "topic_form-content": "new",
            "post_form-content": "dorem ipsum",
            "post_form-user_name": "foobar fez",
            "post_form-user_email": "foo@bar.com",
        }
        self.validAPI=json.dumps({
            "topic":{"content":"apitopic"},
            "question": {
                            "user_name":"apiuser",
                            "user_email":"api@user.com",
                            "content":"apipost"
                        }
        })
        
        self.invalid={
        }
        self.t=Topic(content="Test")
        self.t.save()
        self.p=PostModel(topic=self.t,user_email="foo@bar.com",user_name="foo bar",content="Test Text")
        self.p.save()
        
    def test_get(self):
        resp=self.client.get(reverse("startpage"))
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp.context["topics"].first().content,self.t.content)
        #assert we get initial topic
    def test_get_api(self):
        #same as get
        resp=self.client.get(reverse("api_startpage"))
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp.content,b'{"topics": [{"id": 1, "content": "Test"}]}')

    def test_post_valid(self):
        resp=self.client.post(reverse("startpage"),self.validForm)
        self.assertEqual(resp.status_code,302)
        self.assertEqual( resp._headers["location"][1],"/2")

    def test_post_invalid(self):
        resp=self.client.post(reverse("startpage"),self.invalid)
        self.assertEqual(resp.status_code,200)
        self.assertFalse(resp.context["topic_form"].is_valid())

    def test_post_api_valid(self):
        resp=self.client.post(reverse("api_startpage"),self.validAPI, content_type="application/json")
        self.assertEqual(resp.status_code,200)

    def test_post_api_invalid(self):
        resp=self.client.post(reverse("api_startpage"),json.dumps(self.invalid), content_type="application/json")
        self.assertEqual(resp.status_code,400)
        self.assertEqual(resp.content,b'{"success": false, "errors": {"topic_form": {"content": ["This field is required."]}, "post_form": {"content": ["This field is required."], "user_name": ["This field is required."], "user_email": ["This field is required."]}}}')

    def test_put_invalid(self):
        resp=self.client.put(reverse("api_startpage"))
        self.assertEqual(resp.status_code,403)

class TestTopic(TestCase):
    def setUp(self):
        self.validForm={
                        "content": "formanswer",
                        "user_name": "formuser",
                        "user_email": "form@mail.com"
                       }
        self.invalid={}
        self.validAPI=json.dumps({
                        "answer": {
                            "user_name":"apiuser",
                            "user_email":"api@mail.com",
                            "content":"apipost"
                        }
        })
        self.t=Topic(content="Test")
        self.t.save()
        self.t2=Topic(content="Test2")
        self.t2.save()
        self.p=PostModel(topic=self.t,user_email="foo@bar.com",user_name="foo bar",content="Test Text")
        self.p.original_post=True
        self.p.save()
        self.p2=PostModel(topic=self.t,user_email="foo@bar.com",user_name="foo bar",content="Test Text2")
        self.p2.save()

    def test_404_if_not_topic(self):
        resp=self.client.get(reverse("topic",kwargs={"topic_id":1000}))
        self.assertEqual(resp.status_code,404)
        resp=self.client.post(reverse("topic",kwargs={"topic_id":1000}))
        self.assertEqual(resp.status_code,404)

    def test_get(self):
        resp=self.client.get(reverse("topic",kwargs={"topic_id":self.t.id}))
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp.context["topic"], self.t)
    
    def test_404_if_not_answer(self):
        resp=self.client.get(reverse("update_answer",kwargs={"topic_id":self.t.id,"postm_id":1000}))
        self.assertEqual(resp.status_code,404)

    def test_get_answer(self):
        resp=self.client.get(reverse("update_answer",kwargs={"topic_id":self.t.id,"postm_id":self.p2.id}))
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp.context["post_form"].initial['id'], self.p2.id)
    
    def test_get_api(self):
        resp=self.client.get(reverse("api_topic",kwargs={"topic_id":self.t.id}))
        self.assertEqual(resp.status_code,200)
        data=json.loads(resp.content)["data"][0]
        self.assertEqual(data["id"],self.t.id)
        self.assertEqual(data["content"],self.t.content)
        self.assertEqual(data["posts"],[self.p.id,self.p2.id])
        
    def test_get_answer_api(self):
        resp=self.client.get(reverse("api_update_answer",kwargs={"topic_id":self.t.id,"postm_id":self.p2.id}))
        self.assertEqual(resp.status_code,200)
    
    def test_get_op(self):
        resp=self.client.get(reverse("update_answer",kwargs={"topic_id":self.t.id,"postm_id":self.p.id}))
        self.assertEqual(resp.status_code,400)
    
    def test_get_cross(self):
        resp=self.client.get(reverse("update_answer",kwargs={"topic_id":self.t2.id,"postm_id":self.p2.id}))
        self.assertEqual(resp.status_code,400)
    
    def test_post_valid(self):
        resp=self.client.post(reverse("topic",kwargs={"topic_id":self.t.id}),self.validForm)
        self.assertEqual(resp.status_code,200)
        self.assertEqual(len(resp.context["posts"]),3)
    
    def test_post_invalid(self):
        resp=self.client.post(reverse("topic",kwargs={"topic_id":self.t.id}),self.invalid)
        self.assertEqual(resp.status_code,200)
        self.assertEqual(len(resp.context["post_form"].errors),3)
    
    def test_post_update(self):
        resp=self.client.post(reverse("update_answer",kwargs={"topic_id":self.t.id,"postm_id":self.p2.id}),self.validForm)
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp.context["posts"].filter(id=self.p2.id).first().content,"formanswer")
    
    def test_post_op(self):
        resp=self.client.post(reverse("update_answer",kwargs={"topic_id":self.t.id,"postm_id":self.p.id}),self.validForm)
        self.assertEqual(resp.status_code,400)
    
    def test_post_cross(self):
        resp=self.client.post(reverse("update_answer",kwargs={"topic_id":self.t2.id,"postm_id":self.p.id}),self.validForm)
        self.assertEqual(resp.status_code,400)
    
    def test_post_api_valid(self):
        resp=self.client.post(reverse("api_topic",kwargs={"topic_id":self.t.id}),self.validAPI, content_type="application/json")
        self.assertEqual(resp.status_code,200)

    def test_post_api_invalid(self):
        resp=self.client.post(reverse("api_topic",kwargs={"topic_id":self.t.id}),json.dumps(self.invalid), content_type="application/json")
        self.assertEqual(resp.status_code,400)
        self.assertEqual(resp.content,b'{"success": false, "errors": {"post_form": {"content": ["This field is required."], "user_name": ["This field is required."], "user_email": ["This field is required."]}}}')

    def test_post_api_update(self):
        resp=self.client.post(reverse("api_update_answer",kwargs={"topic_id":self.t.id,"postm_id":self.p2.id}),self.validAPI, content_type="application/json")
        self.assertEqual(resp.status_code,200)
        self.assertEqual(self.t.postmodel_set.filter(id=self.p2.id).first().content,"apipost")
