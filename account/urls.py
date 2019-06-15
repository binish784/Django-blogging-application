from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name='account'

urlpatterns = [
	path('profile/<int:user_id>',views.ProfileView,name='account-profile'),
	path('register/',views.register,name='register'),
	path('login/',auth_views.login,name='login'),
	path('logout/',auth_views.logout,name='logout'),
	path('ajax/validateUsername',views.validate_username,name='validate_username'),
	path('ajax/validateEmail',views.validate_email,name='validate_email'),
	path('editprofile/<int:user_id>',views.editProfile,name='edit_user_profile'),
]
