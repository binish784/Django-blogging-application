from django.urls import path,include
# from .routers import router
from . import views

app_name='post'

urlpatterns = [
	path('',views.IndexView,name='post-home'),
	path('post/create',views.CreateView,name='post-create'),
	path('post/pinned',views.PinnedView,name='post-pinned'),
	path('post/<slug>',views.DetailView,name='post-detail'),
	path('post/<int:post_id>/get_comments',views.GetComment,name='get-comments'),
	path('post/<int:post_id>/update',views.UpdateView,name='post-update'),
	path('post/<int:post_id>/delete',views.DeleteView,name='post-delete'),
	path('post_pin/<int:post_id>',views.PinPost,name='post-pin'),
	path('post/<post_id>/comment',views.PostComment,name='post-comment'),
#	path('api/',include(router.urls)),
	path('api/',include('post.api.urls',namespace="post-api")),
]
