from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.http import request

def verification_email(email,token):
        user = User.objects.get(email=email)
        relative_links = reverse('account:email-verify')
        absurl = 'http://127.0.0.1:8000' +relative_links+'?token='+str(token)
        context = {
            'absurl': absurl,
            'first_name': user.first_name.capitalize(),
            'last_name': user.last_name.lower(),
            'redirect': 'http://127.0.0.1:8000',
            'token':str(token)
        }
        user.email_user(subject='Email Verification',
                        from_email='tradeit <donotreplay@tradeit.com>',
                        template='emails/verify-email.html',
                        context=context,
                        to=email
                        )
        print(f'email has been sent to {email}')