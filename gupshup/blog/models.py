from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

Category_choices = ( 
    ("Technology", "Technology"), 
    ("Mechanical", "Mechanical"), 
    ("Electronic", "Electronic"), 
	("Sports", "Sports"),
	("Business", "Business"),
	("Announcments", "Announcments"),
	("Cultural", "Cultural"),
	("Politics", "Politics"),
	("Health", "Health"),
	("Travel", "Travel"),
	("Fashion", "Fashion"),
	("Miscellenous", "Miscellenous"),

     
)

class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	
	
	category = models.CharField( 
        max_length = 20, 
        choices = Category_choices, 
        default = 'Miscellenous'
        ) 

	def __str__(self):
		return self.title


	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk' : self.pk})

	likes = models.ManyToManyField(User, related_name = 'post_like')
	num_likes = models.IntegerField(default=0)

	def number_of_likes(self):
		return self.likes.count()
		

	# def save(self, *args, **kwargs):
		
	# 	self.num_likes= self.number_of_likes()
	# 	super(Post, self).save(*args, **kwargs)
	
	

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
