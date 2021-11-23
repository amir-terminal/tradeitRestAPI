#Django imports 
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.signals import user_logged_in
#My Imports
from .models import Profile, User
from .utils import verification_email
from .models import IPAddress
from  datetime import datetime
""" 
User profile creation signal 

"""

@receiver(post_save, sender=User)
def create_profile(sender, created, instance, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        email = instance.email
        token = RefreshToken.for_user(instance).access_token
        verification_email(email,token)
        print('Profile has been created')

""" 
User profile updating signal 

"""

@receiver(post_save, sender=User)
def update_profile(sender, created, instance, **kwargs):
    if not created:
        
        instance.profile.save()
        print('Profile has been updated')






@receiver(user_logged_in)
def save_ip(sender, request, user, *args, **kwargs):
    obj, created = IPAddress.objects.get_or_create(user=user,
        IPAddress=request.META.get('X-Real-IP') or request.META.get('REMOTE_ADDR') or '127.0.0.1')
    if not created:
        obj.last_login = datetime.now()
        obj.save()
