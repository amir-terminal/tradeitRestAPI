from .models import BillingAddress,IPAddress
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from leaflet.admin import LeafletGeoAdmin

from .models import Location, Profile, User, BillingAddress, IPAddress

admin.site.site_header = 'tradeit'

"""
Profile Admin
"""

class BillingAddressAdmin(admin.StackedInline):
    model = BillingAddress



class IPAddressAdmin(admin.StackedInline):
    model= IPAddress
    readonly_fields = ('last_login', 'IPAddress')

class ProfileAdmin(admin.StackedInline):
    model = Profile
    followers = Profile.get_profile_followers
    fieldsets = ((None, {'fields': ('trades',
                                    'bought', 'selled')}),
                 ('Settings', {'fields': ('language',
                                          )},),
                 ('Confirmations', {'fields': ('confirmed_phone', 'confirmed_email', 'payment_verified', 'is_trusted'
                                               )})
                 )
    readonly_fields = ('followers', 'trades',
                                    'bought', 'selled', 'language', 'confirmed_phone', 'confirmed_email', 'is_trusted', 'payment_verified')
    extra = 0


"""
Users admin 
"""


@admin.register(User)
class UserAdminConfig(UserAdmin):
    inlines = [ProfileAdmin, IPAddressAdmin]
    search_fields = ['email', 'username', 'last_name']
    list_filter = [
        'email', 'username', 'is_staff', 'is_superuser', 'is_active'
    ]
    ordering = ('-started_date', )
    list_display = [
        'username', 'email', 'first_name', 'last_name', 'is_verified', 'is_active', 'is_staff'
    ]
    fieldsets = (
        (None, {'fields': ('username', 'email',
                           'first_name', 'last_name', 'gender', 'password', 'started_date')}),
        ('Permission', {'fields': ('is_staff',
                                   'is_active', 'is_verified', 'is_superuser')}),
        ('Personel', {'fields': ('birthdate', 'about', 'phone', 'avatar')}),)
    formfield_overrides = {
        User.phone: {
            'title': '+213 5555 5555 55'
        }
    }

    readonly_fields = ('is_staff', 'is_active', 'is_verified', 'is_superuser',
                       'about', 'started_date', 'profile')
    add_fieldsets = [
        (
            None,
            {
                'classes': 'wide',
                'fields': ['first_name', 'last_name', 'username', 'email', 'gender', 'phone', 'birthdate', 'password1', 'password2']
            }
        )
    ]


@admin.register(Location)
class LocationAdmin(LeafletGeoAdmin):
    list_display = ['country', 'state', 'city', 'location_points']
