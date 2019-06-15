from django.shortcuts import render,get_object_or_404
from django.forms.models import model_to_dict

from django.http import HttpResponse,HttpResponseRedirect,Http404,JsonResponse
from django.urls import reverse,reverse_lazy

from django.core import serializers
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

from django.contrib.auth.decorators import login_required

from .forms import PostForm,CommentForm
from .models import post,pinned,comment
import random
# Create your views here.


def IndexView(request):
	posts=post.objects.order_by('-id')
	recent_posts=post.objects.order_by('-id')[:5]
	most_viewed=post.objects.order_by('-views')[:5]
	has_pinned=False
	paginator=Paginator(posts,4)
	page=request.GET.get('page')
	posts=paginator.get_page(page)
	if(len(posts)!=0):
		rand_post=posts[random.randint(0,len(posts)-1)]
	else:
		rand_post=None
	context={
		'rand_post':rand_post,
		'posts':posts,
		'recents':recent_posts,
		'most_views':most_viewed,
	}
	if(request.user.is_authenticated):
		for p in posts:
			if(request.user.pinned_set.filter(pin_post=p)):
				p.pin=True
				if not(has_pinned):
					has_pinned=True
					latest_pinned=pinned.objects.filter(user=request.user).order_by('-pk')[:1]
					latest_pinned=(latest_pinned[0].pin_post)
					context['latest_pinned']=latest_pinned
	context['has_pinned']=has_pinned
	return render(request,'post/index.html',context)



def DetailView(request,slug):
	selected_post=get_object_or_404(post,slug=slug)
	selected_post.views=selected_post.views + 1
	selected_post.save()
	if selected_post.user == request.user:
		context={
			'post':selected_post,
			'flag':1,
		}
	else:
		context={
			'post':selected_post,
		}
	comments=selected_post.comment_set.all().order_by('-pk')
	context['comments']=comments
	context['form']=CommentForm()
	context['title']='Blog-IT : '+selected_post.title
	return render(request,'post/detail.html',context)



@login_required
def PostComment(request,post_id):
	comment_text=request.GET.get('comment_text',None)
	selected_post=get_object_or_404(post,pk=post_id)
	c=comment(comment_text=comment_text)
	c.post=selected_post
	c.user=request.user
	c.save()
	data={
		'message':'Comment Posted'
	}
	return JsonResponse(data)


def GetComment(request,post_id):
	selected_post=get_object_or_404(post,pk=post_id)
	data_set=[]
	comments=selected_post.comment_set.all().order_by('-pk')
	for i,comment in enumerate(comments):
		username=comment.user.username
		user_id=comment.user.id
		user_pic=comment.user.profile.image.url
		comment_text=comment.comment_text
		data={
			'user_id':user_id,
			'username':username,
			'image':user_pic,
			'comment':comment_text,
		}
		data_set.append(data)
	json_data={
		'comments':data_set
	}
	return JsonResponse(json_data)


@login_required
def CreateView(request):
	if request.POST:
		form=PostForm(request.POST,request.FILES)
	else:
		form=PostForm(None)
	if form.is_valid():
		instance=form.save(commit=False)
		instance.user=request.user
		instance.save()
		return HttpResponseRedirect(reverse_lazy('post:post-detail',kwargs={'slug':instance.slug}))
	context={
		'form':form,
	}
	return render(request,'post/create.html',context)

@login_required
def UpdateView(request,post_id):
	selected_post=get_object_or_404(post,pk=post_id)
	if selected_post.user != request.user:
		raise Http404
	form=PostForm(request.POST or None,instance=selected_post)
	
	if form.is_valid():
		instance=form.save(commit=False)
		instance.save()
		return HttpResponseRedirect(reverse_lazy('post:post-detail',kwargs={'post_id':instance.id}))
	context={
		'title':'Update : '+selected_post.title,
		'post':selected_post,
		'form':form,
	}
	return render(request,'post/update.html',context)

@login_required
def DeleteView(request,post_id):
	selected_post=get_object_or_404(post,pk=post_id)
	if selected_post.user != request.user:
		raise Http404
	context={
		'title':'Confirm deletion : '+selected_post.title,
		'post':selected_post,
	}
	if request.POST:
		selected_post.delete()
		return HttpResponseRedirect(reverse_lazy('post:post-home'))
	return render(request,'post/delete.html',context)

@login_required
def PinPost(request,post_id):
	selected_post=get_object_or_404(post,pk=post_id)
	if(request.user.pinned_set.filter(pin_post=selected_post)):
		query_set=request.user.pinned_set.filter(pin_post=selected_post)[:1]
		instance=query_set[0]
		instance.delete()
		return HttpResponseRedirect(reverse_lazy('post:post-home'))
	instance=pinned(pin_post=selected_post,user=request.user)
	instance.save()
	return HttpResponseRedirect(reverse_lazy('post:post-detail',kwargs={'slug':selected_post.slug}))

@login_required
def PinnedView(request):
	pin_set=request.user.pinned_set.all().order_by('-pk')
	if not(pin_set):
		raise Http404
	pinned_set=[]
	for p in pin_set:
		p.pin=True
		pinned_set.append(p.pin_post)
	context={
		'pinned_posts':pinned_set
	}
	return render(request,'post/pinned.html',context)

