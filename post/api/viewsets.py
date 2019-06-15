
from django.db.models import Q

from post.models import post

from .serializers import PostSerializer,PostCreateSerializer,PostDetailSerializer


from rest_framework import viewsets

from rest_framework.filters import (
	SearchFilter,
	OrderingFilter,
)

from rest_framework.permissions import (
	IsAuthenticated,
	IsAdminUser,
	AllowAny,
	IsAuthenticatedOrReadOnly,
)

from rest_framework.generics import (
	ListAPIView,
	RetrieveAPIView,
	UpdateAPIView,
	DestroyAPIView,
	CreateAPIView,
	)

from .permissions import IsOwnerOrReadOnly

class PostCreateAPIView(CreateAPIView):
	queryset=post.objects.all()
	serializer_class=PostCreateSerializer
	permission_classes=[IsAuthenticated]

	def perform_create(self,serializer):
		serializer.save(user=self.request.user)

class PostListAPIView(ListAPIView):
	queryset=post.objects.all()
	serializer_class=PostSerializer
	filter_backends=[SearchFilter,OrderingFilter]
	search_fields=['title','content','user__first_name','user__last_name']

	def get_queryset(self,*args,**kwargs):
		queryset_list=post.objects.all()
		query=self.request.GET.get('q')
		if query:
			queryset_list= queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query)|
				Q(user__last_name__icontains=query)
				).distinct()
		return queryset_list

class PostDetailAPIView(RetrieveAPIView):
	queryset=post.objects.all()
	serializer_class=PostDetailSerializer

class PostUpdateAPIView(UpdateAPIView):
	queryset=post.objects.all()
	serializer_class=PostSerializer
	permission_classes=[IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]

	def perform_update(self,serializer):
		serializer.save(user=self.request.user)


class PostDestroyAPIView(DestroyAPIView):
	queryset=post.objects.all()
	serializer_class=PostSerializer
	permission_classes=[IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]


