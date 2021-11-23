from django.contrib.auth.forms import UserCreationForm
from django.db.models import fields
from .models import User
# from django import forms

""" User creation form """
class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','phone','birthdate','password1','password2','avatar']
        
        


# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext as _
from django.contrib.admin import widgets



from .models import BillingAddress


class BillingForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        exclude = ('user','deleted','shipping')

class DateRangeForm(forms.Form):
    """Form for selection date range """

    start_date = forms.DateField(label=_('Start date'), widget=widgets.AdminDateWidget())
    end_date = forms.DateField(label=_('End date'), widget=widgets.AdminDateWidget())


class DeleteForm(forms.Form):
    pk = forms.IntegerField()

