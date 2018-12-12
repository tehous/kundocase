from django.db import models
from django.utils import timezone
from kundocase.forum.spamcheck import spamcheck
#from .spamcheck import ...

class SpamFilterManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        qs = super(SpamFilterManager, self).get_queryset(*args, **kwargs)
        return qs.filter(is_spam=False)

class Topic(models.Model):
    content = models.CharField("Title",max_length=255)
    last_post=models.DateTimeField(default=timezone.now)
    is_spam=models.BooleanField(default=False)
    objects=SpamFilterManager()
    adminmanager=models.Manager()
    class Meta:
        ordering=["-last_post"]

    def save(self,*args,**kwargs):
        if spamcheck(self):
            self.is_spam=True
        super(Topic,self).save(*args,**kwargs)
    def __str__(self):
        return str(self.content)

class PostModel(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    content = models.TextField()
    user_name = models.CharField(max_length=255)
    user_email = models.EmailField(max_length=255)
    original_post=models.BooleanField(default=False)
    created=models.DateTimeField(default=timezone.now)
    is_spam=models.BooleanField(default=False)
    objects=SpamFilterManager()
    adminmanager=models.Manager()
    #could add updated=date
    #could add fk to self to enable post nesting
    class Meta:
        ordering=["-original_post","created"]

    def save(self,*args,**kwargs):
        if self.topic.is_spam or spamcheck(self):
            self.is_spam=True
            if self.original_post:
                self.topic.is_spam=True
        self.topic.last_post=self.created
        self.topic.save()
        super(PostModel,self).save(*args,**kwargs)
    
    def __str__(self):
        return str(self.topic)+":"+str(self.id)
