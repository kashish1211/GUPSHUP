from django.db import models
from django.contrib.auth.models import User
from PIL import Image


gender_choices = (
    ("Male", "Male"),
    ("Female", "Female"),
    ("Others", "Others"),
)

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='default.jpg',upload_to='profile_pics')
	gender = models.CharField(max_length = 20,choices=gender_choices,default='Select your gender',blank=True, null=True)
	def __str__(self):
		return f'{self.user.username} Profile '

	def save(self,*args,**kwargs):
		super().save(*args,**kwargs)

		img = Image.open(self.image.path)

		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.image.path)



	# def save_profile(backend, user, response, *args, **kwargs):
	# 	if backend.name == 'facebook':
	# 		profile = user.get_profile()
	# 		if profile is None:
	# 			profile = Profile(user_id=user.id)
	# 		profile.gender = response.get('gender')
	# 		profile.link = response.get('link')
	# 		profile.timezone = response.get('timezone')
	# 		profile.save()