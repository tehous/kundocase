from django.forms import ModelForm
from .models import Topic,PostModel

class TopicForm(ModelForm):
    class Meta:
        model=Topic
        fields=[
                'content'
               ]
        
class PostForm(ModelForm):
    class Meta:
        model=PostModel
        fields=[
                 'content',
                 'user_name',
                 'user_email',
                ]


