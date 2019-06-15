from django.shortcuts import render,get_object_or_404,redirect

from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.http import HttpResponseRedirect,HttpResponse,JsonResponse,Http404
from django.urls import reverse,reverse_lazy

from .forms import UserForm,ProfileForm,UserUpdateForm
from post.models import post

# Create your views here.


def register(request):
	form=UserForm(request.POST or None)
	if form.is_valid():
		user=form.save(commit=False)
		username=form.cleaned_data['username']
		password=form.cleaned_data['password']
		user.set_password(password)
		user.save()
		user=authenticate(username=username,password=password)
		login(request,user)
		return HttpResponseRedirect(reverse_lazy('account:edit_user_profile',kwargs={'user_id':user.id}))
	context={
		'title':'Blog-IT : Register',
		'form':form
	}
	return render(request,'account/register.html',context)

@login_required
def ProfileView(request,user_id):
	selected_user=User.objects.get(id=user_id)
	posts=post.objects.filter(user=selected_user).order_by('-pk')
	if(posts):
		context={
			'title':'Profile : '+selected_user.username,
			'posts':posts,
		}
	else:
		context={
			'title':'Profile : '+selected_user.username
		}
	return render(request,'account/profile.html',context)


def validate_username(request):
	username=request.GET.get('username',None)
	data = {
		'is_taken':User.objects.filter(username__iexact=username).exists(),
	}
	if data['is_taken']:
		data['message']='A user with username '+username+' already exists'
	return (JsonResponse(data))

def validate_email(request):
	email=request.GET.get('email',None)
	data={
		'is_taken':User.objects.filter(email__iexact=email).exists(),
	}
	if data['is_taken']:
		data['message']='An account with this email already exists'
	return JsonResponse(data)

@login_required
def editProfile(request,user_id):
	selected_user=get_object_or_404(User,pk=user_id)
	if request.user!=selected_user:
		raise Http404
	userform=UserUpdateForm(request.POST or None,instance=selected_user)
	profileform=ProfileForm(request.POST or None, request.FILES,instance=selected_user.profile)
	
	if userform.is_valid() and profileform.is_valid():
		u_instance=userform.save(commit=False)
		p_instance=profileform.save(commit=False)
		u_instance.save()
		p_instance.save()
		messages.success(request,"Your Profile Has been Updated")
		print(user_id)
		return redirect('account:account-profile',user_id)
	context={
		'title':'Profile : '+selected_user.username,
		'userform':userform,
		'profileform':profileform,
	}
	return render(request,'account/editProfile.html',context)