from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import urllib.request
import os
from django.core.files import File
from urllib.request import urlopen
from tempfile import NamedTemporaryFile
from ckeditor.fields import RichTextField
from blog.models import Category
import os



college_choices = (
	("KJSCE", "KJSCE"),
	("Aurobindo", "Aurobindo"),
	("Chanakya", "Chanakya"),
	
)


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='default2.png',upload_to='profile_pics')
	college = models.CharField(max_length = 20,choices=college_choices,default='KJSCE',blank=True, null=True)
	about = RichTextField(blank=True, null=True)
	followed_category = models.ManyToManyField(Category,related_name='followed_category',blank=True, null=True)
	
	image_url = models.URLField(default = "http://127.0.0.1:8000/media/default2.png")
	def __str__(self):
		return f'{self.user.username} Profile '


	def get_remote_image(self):
		if self.image_url and self.image == 'default2.png':
			result = urllib.request.urlretrieve(self.image_url)
			self.image.save(
					os.path.basename(self.image_url),
					File(open(result[0], 'rb'))
					)
			self.save()

	def save(self,*args,**kwargs):
		super(Profile, self).save(*args, **kwargs)
		
		img = Image.open(self.image.path)

		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.image.path)





