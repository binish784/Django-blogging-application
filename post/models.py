from django.db import models

from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

from third.utils import unique_slug_generator
from django.db.models.signals import pre_save
from django.dispatch import receiver

class post(models.Model):
	title=models.CharField(max_length=200)
	content=models.TextField(max_length=1000)
	pub_date=models.DateTimeField(default=timezone.now)
	user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,default=1)
	pin=models.BooleanField(default=False)
	image=models.ImageField()
	views=models.IntegerField(default=0)
	slug=models.SlugField(unique=True,max_length=200)

	def __str__(self):
		return self.title + " : " + self.content[:20]

	@property
	def get_comments(self):
		return self.comment_set.all()

	@property
	def comment_count(self):
		count=self.comment_set.all().count()
		return count

@receiver(pre_save,sender=post)
def slug_save(sender,instance, *args, **kwargs):
	if not instance.slug:
		instance.slug=unique_slug_generator(instance,instance.title,instance.slug)

class pinned(models.Model):
	pin_post=models.ForeignKey(post,on_delete=models.CASCADE)
	user=models.ForeignKey(User,on_delete=models.CASCADE)

	def __str__(self):
		return self.pin_post.title + " : " + self.user.username
 
class comment(models.Model):
	post=models.ForeignKey(post,on_delete=models.CASCADE)
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	comment_text=models.CharField(max_length=200)

	def __str__(self):
		return self.user.username + " : " + self.comment_text  