from django.test import TestCase

from django.contrib.auth.models import User

from .models import post
# Create your tests here.

class TestingSlugField(TestCase):

	def setUp(self):
		user1=User.objects.create(username='asd',password='qwerty');
		p1=post.objects.create(title='Title goes here',user=user1);
		p2=post.objects.create(title='Title goes here',user=user1);
		
	def test_slug_uniqness(self):
		p1=post.objects.get(pk=1);
		p2=post.objects.get(pk=2);
		self.assertEqual(p1.slug,'title-goes-here');
		self.assertEqual(p2.slug,'title-goes-here-2');

