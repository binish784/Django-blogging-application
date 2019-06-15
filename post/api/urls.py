from django.urls import path,include
# from .routers import router
from .viewsets import (
	PostListAPIView,
	PostDetailAPIView,
	PostUpdateAPIView,
	PostDestroyAPIView,
	PostCreateAPIView,
	)

app_name='api'

urlpatterns = [
	path('post/',PostListAPIView.as_view(),name='list'),
	path('post/create',PostCreateAPIView.as_view(),name='create'),
	path('post/<pk>',PostDetailAPIView.as_view(),name='detail'),
	path('post/<pk>/update',PostUpdateAPIView.as_view(),name='update'),
	path('post/<pk>/delete',PostDestroyAPIView.as_view(),name='delete'),
]
