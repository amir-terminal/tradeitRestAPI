from django.urls import path
from apps.views import VerifyEmail

app_name = 'account'
urlpatterns = [
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
]
