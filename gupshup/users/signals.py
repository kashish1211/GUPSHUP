from django.db.models.signals import post_save
from django.contrib.auth.models import User
from notifications.signals import notify
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_proile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)



@receiver(post_save, sender=User)
def save_proile(sender, instance, **kwargs):
	instance.profile.save()


# def my_handler(sender, instance, created, **kwargs):
#     notify.send(instance, verb='was saved')

# post_save.connect(my_handler, sender=User)
