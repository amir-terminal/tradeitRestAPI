"""
Django Imports
"""
from .models import BillingAddress, IPAddress, Profile, User
from .utils import verification_email
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import fields, serializers
from django.core.validators import ip_address_validator_map
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


"""
Third Party imports
"""
"""
My Imports
"""
# from .utils import resendEmail

""" ********************************** Code *********************************************** """


class BillingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingAddress
        fields = ['address1', 'address2', 'country', 'city', 'state', 'zipcode',
                  'created',
                  ]

"""
User profile serializer

"""


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['followers', 'trades', 'bought', 'selled', 'language',
                  'payment_verified', 'confirmed_facebook', 'confirmed_email', 'is_trusted', 'created_at', 'updated_at', ]


"""
User serializer


"""


class UserSerializer(serializers.ModelSerializer):
    ip_address = serializers.StringRelatedField(source='ip_addresses')
    email = serializers.EmailField(max_length=255, min_length=2)
    username = serializers.CharField(max_length=150)
    phone = serializers.CharField(max_length=15)
    password = serializers.CharField(
        max_length=65, min_length=8, write_only=True)
    first_name = serializers.CharField(max_length=100,)
    last_name = serializers.CharField(max_length=100,)
    avatar = serializers.ImageField('get_image_url')
    profile = ProfileSerializer(read_only = True)
    billing_addresses = BillingAddressSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'birthdate', 'gender', 'phone', 'password', 'avatar', 'ip_address', 'billing_addresses','profile']

    def avatar(self, obj):
        return obj.avatar.url



""" Email Verification Serializer """


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)
    class Meta:
        model = User
        fields = ['token']
        
class UserExistSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    username = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    avatar = serializers.ImageField()
    
    def avatar(self, obj):
        return obj.avatar.url
    
    class Meta:
        model = User
        fields = ['email','username',"first_name",'last_name','avatar']
        
    

    
    def validate(self, attrs):
        email = attrs.get('email', '')
        user = User.objects.get(email = email)
        if user: 
            return {
                'id':user.id,
                'username':user.username,
                'email':user.email,
                'first_name':user.first_name,
                'last_name':user.last_name,
                'avatar':user.avatar,
            }
        




"""
User Login Serializer
"""


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    username = serializers.CharField(read_only=True)
    tokens = serializers.SerializerMethodField()
    
    

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = User
        fields = ['id','email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        password = attrs.get('password', '')
        # filtered_user_by_email = User.objects.filter(email=email)
        if username != '':
            user = User.objects.get(usname=username)
            email = user.email
            return email
        user = authenticate(email=email, password=password)

        # if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
        #     raise AuthenticationFailed(
        #         detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_verified:
            token = RefreshToken.for_user(user).access_token
            verification_email(email, token)
            raise AuthenticationFailed(
                'Email is not verified,a new verification email has been sent your inbox\n\n please check your inbox')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }
        
        return super().validate(attrs)



class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=2)
    username = serializers.CharField(max_length=150)
    phone = serializers.CharField(max_length=15)
    password = serializers.CharField(
        max_length=65, min_length=8, write_only=True)
    first_name = serializers.CharField(max_length=100,)
    last_name = serializers.CharField(max_length=100,)
    avatar = serializers.ImageField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name',
                  'birthdate', 'gender', 'phone', 'password','avatar']
    

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        phone = attrs.get('phone', '')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                _('Username already in use, would you like to try to login'))
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                _('Email already in use,  would you like to try to login'))
        if User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError(
                _('Phone number already in use,  would you like to try to login'))
        return attrs

    def create(self, validated_data):
        password = validated_data.get('password')
        validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
    


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)
    redirect_url = serializers.CharField(max_length=500, required=False)
    class Meta:
        fields = ['email']
        
        
class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)



    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)
