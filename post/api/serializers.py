from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from post.models import post,comment
from django.contrib.auth.models import User

class PostSerializer(serializers.ModelSerializer):
	# url=HyperlinkedIdentityField(
	# 		view_name='post-api:detail',
	# 		lookup_field='pk'
	# 	)
	user=SerializerMethodField()
	class Meta:
		model=post
		fields=[
			'id',
			'user',
			'title',
			'content',
			'image',
			'views',
			'pin',
			'pub_date'
		]
	def get_user(self,obj):
		return str(obj.user.username)

	def get_image(self,obj):
		try:
			return obj.image.url
		except:
			return None

class PostDetailSerializer(serializers.ModelSerializer):
	image=SerializerMethodField()
	comments=SerializerMethodField()
	
	class Meta:
		model=post
		fields=['user','title','content','image','views','pin','pub_date','comments']
	def get_user(self,obj):
		return obj.user.username

	def get_image(self,obj):
		try:
			return obj.image.url
		except:
			return None

	def get_comments(self,obj):
		object_id=obj.id
		c_qs=obj.get_comments
		comments=CommentSerializer(c_qs,many=True).data
		return comments

class PostCreateSerializer(serializers.ModelSerializer):
	image=SerializerMethodField()
	class Meta:
		model=post
		fields=['title','content','image','pin','pub_date']

class CommentSerializer(serializers.ModelSerializer):
	user=SerializerMethodField()
	
	class Meta:
		model=comment
		fields=['user','comment_text']

	def get_user(self,obj):
		return obj.user.username