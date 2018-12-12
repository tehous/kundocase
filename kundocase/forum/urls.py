from django.conf.urls import url
from kundocase.forum.views import topicListview, topicView

urlpatterns = [
    url(r"^$", topicListview, name="startpage"),
    url(r"^api$", topicListview, name="api_startpage", kwargs={"api_call":True}),
    
    url(r"^(?P<topic_id>\d+)$", topicView, name="topic"),
    url(r"^(?P<topic_id>\d+)/(?P<postm_id>\d+)",topicView,name="update_answer"),
    
    url(r"^api/(?P<topic_id>\d+)$", topicView, name="api_topic",kwargs={"api_call":True}),
    url(r"^api/(?P<topic_id>\d+)/(?P<postm_id>\d+)",topicView,name="api_update_answer",kwargs={"api_call":True}),
]
