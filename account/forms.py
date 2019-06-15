from django import forms

from django.contrib.auth.models import User
from .models import Profile

class UserForm(forms.ModelForm):

	password=forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model=User
		fields=['username','email','password']


class UserUpdateForm(forms.ModelForm):

	class Meta:
		model=User
		fields=['username','first_name','last_name','email']

class ProfileForm(forms.ModelForm):

	class Meta:
		model=Profile
		fields=['image']