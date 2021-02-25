from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title


	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk' : self.pk})

	likes = models.ManyToManyField(User, related_name = 'post_like')

	def number_of_likes(self):
		return self.likes.count()

	@property
	def number_of_comments(self):
		return PostComment.objects.filter(post_connected = self).count()


class PostComment(models.Model):
	post_connected = models.ForeignKey(Post, related_name = 'comments', on_delete = models.CASCADE)
	author = models.ForeignKey(User, on_delete = models.CASCADE)
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return str(self.author) + ', ' + self.post_connected.title[:40]
