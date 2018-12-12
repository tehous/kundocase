from django.shortcuts import render, get_object_or_404
from kundocase.forum.models import Topic, PostModel
from kundocase.forum.forms import TopicForm,PostForm
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.db import transaction
from django.forms.models import model_to_dict
from django.http.response import JsonResponse
from json import loads
from django.shortcuts import redirect

def topicListview(request, api_call=False):
    if request.method =="GET":
        if id:
            return get_topics(request, api_call)
    elif request.method=="POST":
        return post_topic(request,api_call)
    #default
    raise PermissionDenied

def topicView(request,topic_id, postm_id=None,api_call=False):
    if request.method =="GET":
        return get_topic(request, topic_id, postm_id, api_call)
    elif request.method=="POST":
        return post_post(request, topic_id, postm_id, api_call)
    #default
    raise PermissionDenied


def get_topics(request, api_call=False):
    topics = Topic.objects.all()
    if api_call:
        fields=['id','content']
        return JsonResponse({"topics":list(topics.values(*fields))})
    topic_form=TopicForm(prefix="topic_form")
    post_form=PostForm(prefix="post_form")
    return render(request, "forum/startpage.html", {
        "topics": topics,
        "topic_form":topic_form,
        "post_form":post_form
    })

def api_new_topic_forms(request):
    data=loads(request.body.decode('utf-8'))
    return (TopicForm(data=data.get("topic",{})),PostForm(data=data.get("question",{})))

def post_topic(request,api_call=False):
    if api_call:
        topic_form,post_form=api_new_topic_forms(request)
    else:
        topic_form=TopicForm(request.POST,prefix="topic_form")
        post_form=PostForm(request.POST,prefix="post_form")
    if topic_form.is_valid() and post_form.is_valid():
        with transaction.atomic():
            topic=topic_form.save()
            postm=post_form.save(commit=False)
            postm.topic=topic
            postm.original_post=True
            postm.save()
        if api_call:
            return JsonResponse({'success':True})
        if not topic.is_spam:
            return redirect("topic",topic_id=topic.id)
        else:
            return redirect("startpage")
    if api_call:
        return JsonResponse({'success':False,'errors':{
                             "topic_form":topic_form.errors,
                             "post_form":post_form.errors,
                              }},status=400)

    topics=Topic.objects.all()
    return render(request, "forum/startpage.html", {
        "topics": topics,
        "topic_form":topic_form,
        "post_form":post_form
    })

def get_topic(request, topic_id, postm_id=None, api_call=False):
    topic = get_object_or_404(Topic, id=topic_id)
    postm=None
    if postm_id:
        postm=get_object_or_404(PostModel,id=postm_id)
        if not postm.topic_id == int(topic_id):
            raise SuspiciousOperation("Cannot cross edit QA between topics")
        if postm.original_post:
            raise SuspiciousOperation("Cannot edit original questions")
        if not api_call:
            post_form=PostForm(initial=model_to_dict(postm))
    elif not api_call: 
        post_form=PostForm()
    posts = topic.postmodel_set.all()
    if api_call:
        if postm:
            return JsonResponse({"data":[model_to_dict(postm,exclude=("is_spam"))]})
        else:
            tdict=model_to_dict(topic,exclude=("is_spam"))
            tdict["posts"]=[post.id for post in posts]
            return JsonResponse({"data":[tdict]})
            
    return render(request, "forum/topic.html", {
        "topic": topic,
        "posts": posts,
        "post_form":post_form,
    })

def api_post_form(request):
    data=loads(request.body.decode('utf-8'))
    return (PostForm(data=data.get("answer",{})))

def post_post(request, topic_id, postm_id=None,api_call=False):
    topic = get_object_or_404(Topic, id=topic_id)
    if api_call:
        post_form=api_post_form(request)
    else:
        post_form=PostForm(request.POST)
    if post_form.is_valid():
        if postm_id:
            postm=get_object_or_404(PostModel, id=postm_id)
            if not postm.topic_id == int(topic_id):
                raise SuspiciousOperation("Cannot cross edit QA between topics")
            if postm.original_post:
                raise SuspiciousOperation("Cannot edit original questions")
            postm.content=post_form.cleaned_data["content"]
            postm.user_name=post_form.cleaned_data["user_name"]
            postm.user_email=post_form.cleaned_data["user_email"]
            postm.save()
            if api_call:
                return JsonResponse({'success':True})
        else:
            postm=post_form.save(commit=False)
            postm.topic=topic
            postm.save()
            if api_call:
                return JsonResponse({'success':True})
        post_form=PostForm()

    if api_call:
        return JsonResponse({'success':False,'errors':{
                             "post_form":post_form.errors,
                             }},status=400)

    posts = topic.postmodel_set.all()
    return render(request, "forum/topic.html", {
        "topic": topic,
        "posts": posts,
        "post_form":post_form,
        "postm_id":postm_id
    })
