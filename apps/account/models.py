"""
Django Imports
"""
from django.contrib.auth.signals import user_logged_in
from django.db.models.fields.related import ForeignKey
from rest_framework_simplejwt.tokens import RefreshToken
import uuid as uuid_lib
import os
from datetime import datetime
from datetime import date
from django.db.models.deletion import SET_DEFAULT
from django.db import models
from django.core.cache import cache
from django.core.checks.messages import Error
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.gis.db import models as geo_models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django_countries.fields import CountryField

"""
Third Party imports
"""
"""
My Imports 
"""

""" ********************************** Code *********************************************** """

# Create your models manager here.


class UserManager(BaseUserManager):
    def create_superuser(self, email, username, phone, first_name, last_name,
                         password, birthdate, **other_fields):

        user = self.create_user(email=email,
                                phone=phone,
                                first_name=first_name,
                                last_name=last_name,
                                username=username,
                                password=password,
                                birthdate=birthdate)
        user.is_verified = True
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

    def create_user(self, email, username, phone, first_name, last_name,
                    password, birthdate, **other_fields):
        if not email:
            raise TypeError(_('You must provide an email address'))
        if not username:
            raise TypeError(_('You must provide a username'))
        if not first_name:
            raise TypeError(_('You must provide your first name'))
        if not last_name:
            raise TypeError(_('You must provide your last name'))
        if not phone:
            raise TypeError(_('you must provide a phone number'))
        if not password:
            raise TypeError(_('you must provide a password'))

        """ Email normalize from the baseusermanage lookitup """

        email = self.normalize_email(email)

        """ setting the user model   """
        user = self.model(email=email,
                          username=username,
                          phone=phone,
                          first_name=first_name,
                          last_name=last_name,
                          birthdate=birthdate,
                          **other_fields)
        """ setting the password  """
        user.set_password(password)
        user.save()
        return user


def uploadmodel_file_upload_to(instance, filename):
    filename, file_extension = os.path.splitext(filename)
    return f'uploads/{instance.username}/avatars/{instance.id}{file_extension}'


class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


# Create your models here.
"""
Customized user model for the tradeit app 
"""


class User(AbstractBaseUser, PermissionsMixin):
    GenderChoices = (('f', 'female'), ('m', 'male'),
                     ('none', 'prefered not to say'),)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

    uuid = models.UUIDField(
        db_index=True,
        default=uuid_lib.uuid4,
        editable=False,
        unique=True)
    email = models.EmailField(_('email'), unique=True, db_index=True)
    username = models.CharField(_('Username'),
                                unique=True,
                                db_index=True,
                                max_length=150)
    phone = models.CharField(_('phone number'), validators=[
                             phone_regex], unique=True, max_length=17, db_index=True)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    gender = models.CharField(
        max_length=60, choices=GenderChoices, null=True, default='none')
    birthdate = models.DateField(
        _('date of birth'), blank=False, null=True)
    started_date = models.DateTimeField(default=timezone.now)

    avatar = models.ImageField(
        upload_to=uploadmodel_file_upload_to, default=f'defaults/avatar/none/none.jpg', null=True, blank=True, storage=OverwriteStorage(),)
    about = models.TextField(_('about'), max_length=500, blank=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone',
                       'first_name', 'last_name', 'birthdate', 'gender']

    def avatarimg(self):
        return self.gendertype

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def get_full_name(self):
        firstname = self.first_name.capitalize()
        return f"{firstname} {self.last_name}"

    def get_short_name(self):
        return self.username

    def get_current_age(self):
        today = date.today()
        age = today.year - self.birthdate.year - \
            ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))
        return f'{age} year old'

    def email_user(self, subject, context, template, to, from_email, *args, **kwargs):
        html_message = render_to_string(template, context)
        plain_message = strip_tags(html_message)
        mail.send_mail(subject, plain_message, from_email,
                       recipient_list=[to], html_message=html_message)


"""
Location model
"""


class Location(geo_models.Model):
    user = ForeignKey(User,on_delete=models.CASCADE)
    country = geo_models.CharField(max_length=150, null=True)
    city = geo_models.CharField(max_length=150, null=True)
    state = geo_models.CharField(max_length=150, null=True)
    zipcode = geo_models.CharField(max_length=150, null=True)
    location_points = geo_models.PointField(max_length=40, null=True)
    radius = geo_models.IntegerField(default=20,
                                     help_text="in kilometers", validators=[MinValueValidator(1), MaxValueValidator(1000)])

    def __str__(self):
        return f'{self.state}, {self.country}'


"""
User profile auto created using signals
"""


class Profile(models.Model):
    language_choice = [('ar', 'Arabic'), ('de', 'German'), ('en', 'English'), (
        'es', 'Spanish'), ('fr', 'French'), ('jp', 'Japanese'), ('ch', 'Chinese'),]
    user = models.OneToOneField(
        'User', on_delete=models.CASCADE, db_index=True, editable=False, related_name='profile')
    followers = models.ManyToManyField('Profile',
                                       related_name="followers_profile")
    following = models.ManyToManyField('Profile',related_name='followings_profile')

    trades = models.IntegerField(default=0)
    bought = models.IntegerField(default=0)
    selled = models.IntegerField(default=0)
    # location = models.ForeignKey(
    #     Location, on_delete=models.SET_NULL,null=True)
    language = models.CharField(
        max_length=7, default='en', choices=language_choice)
    payment_verified = models.BooleanField(default=False)
    confirmed_phone = models.BooleanField(default=False)
    confirmed_facebook = models.BooleanField(default=False,)
    confirmed_email = models.BooleanField(default=False)
    is_trusted = models.BooleanField(default=False,)
    created_at = models.DateTimeField(auto_now_add=True,)
    updated_at = models.DateTimeField(auto_now=True)

    def get_profile_followers(self):
        return self.followers.count()

    def last_seen(self):
        return cache.get('last_seen_%s' % self.user.username)
    
    def follow(self,profile):
        pass
    
    def buy(self):
        pass
    
    def trade(self):
        pass
    
    def choose_language(self):
        pass
    
    
    # def bid(self, auction):
    #     auction.bid_by(self)
    #     self.credits -= 1
    #     self.points_amount += User.rewards.bid
    #     self.save()
    

    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > (self.last_seen() + datetime.timedelta(seconds=settings.USER_ONLINE_TIMEOUT)):
                return False
            else:
                return True
        else:
            return False

    def __str__(self):
        return self.user.username


class BillingAddress(models.Model):

    user = models.ForeignKey(
        User, related_name='billing_addresses', on_delete=models.CASCADE)
    address1 = models.CharField(max_length=100,null=True)
    address2 = models.CharField(max_length=100, blank=True)
    country = CountryField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    city = geo_models.CharField(max_length=150, null=True)
    state = geo_models.CharField(max_length=150, null=True)
    zipcode = geo_models.CharField(max_length=150, null=True)

    def __str__(self):
        return f'{self.state}, {self.country}'


    def __unicode__(self):
        return self.user


class IPAddress(models.Model):
    user = models.ForeignKey(
        User, related_name='ip_addresses', on_delete=models.CASCADE)
    IPAddress = models.GenericIPAddressField()
    last_login = models.DateField(default=datetime.now)
    

    def __unicode__(self):
        return IPAddress;

    class Meta:
        unique_together = ('user', 'IPAddress')
        ordering = ('-last_login', )
        verbose_name_plural = 'IP addresses'


# class BannedIPAddress(models.Model):
#     IPAddress = models.GenericIPAddressField()
#     created_at = models.DateField(auto_now_add=True)

#     def __unicode__(self):
#         return self.IPAddress

#     class Meta:
#         app_label = ""
#         db_table = "profiles_bannedipaddress"
#         verbose_name_plural = 'Banned IP addresses'
        
        
# class BannedUser(models.Model):
#     user = models.ForeignKey('user',on_delete=models.CASCADE)
#     created_at = models.DateField(auto_now_add=True)

#     def __unicode__(self):
#         return self.user

#     class Meta:
#         app_label = "auth"
#         db_table = "profiles_bannedipaddress"
#         verbose_name_plural = 'Banned Users'

