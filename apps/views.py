"""************************************ Imports ***************************** """

""" Django Imports """


"""Thrid Party Imports """

# Rest framework
# SimpleJWT
# Swagger api
# PYJwt

""" My Imports """
# Api

# Authentification
# Products

# Messengers

""" ********************************** Code *********************************************** """


# Create your views here.
""" ********************************************** authentification ******************************************************"""

""" Registration API View  """




from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.conf import settings
from django.db.models.query import QuerySet
from rest_framework import permissions
from rest_framework.serializers import Serializer
from rest_framework_simplejwt.tokens import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import jwt
from .permissions import IsOwner
from .account.serializers import *
from .account.models import User
from .account.utils import *
from .product.serializers import AddProductSerializers, CategorySerializer, ProductListSerializer, ProductSerializer
from .product.models import Category, Product
from rest_framework import generics, views, status





# ___________________________________________________________________ Views API __________________________________________________________________________
class RegisterAPIView(generics.GenericAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        # user = User.objects.get(email=user_data['email'])
        # token = RefreshToken.for_user(user).access_token
        # current_site = get_current_site(request).domain
        # relativeLink = reverse('email-verify')
        # absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        # context = {
        #         'absurl': absurl,
        #         'first_name': user_data.get('first_name').capitalize(),
        #         'last_name': user_data.get('last_name').lower()
        #     }
        # user.email_user(subject='Email verification',
        #                     from_email='Tradit no-replay',
        #                     template='emails/verify-email.html',
        #                     context=context,
        #                     to=user_data.get('email')
        #                     )
        return Response(user_data, status=status.HTTP_201_CREATED)


class CurrentUserAPIView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self,request):
        user_id = request.user.id
        profile_data = User.objects.get(id=user_id)
        serializer = self.serializer_class(profile_data)
        return Response(serializer.data,status=200)

""" Email Verification """

class EmailCheck(views.APIView):
    serializer_classes = UserExistSerializer
    permission_classes =  (permissions.AllowAny,)
    
    def post(self, request):
        serializer = self.serializer_classes(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=200)


class VerifyEmail(views.APIView):
    serializer_classes = EmailVerificationSerializer
    permission_classes = (permissions.AllowAny,)
    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.profile.confirmed_email = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired,'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


""" Login API View """


class LoginAPIView(views.APIView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)


""" **********************************************  Products  ******************************************************"""


class ProductsAPIListView(views.APIView):
    serializer_classes = ProductSerializer
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        products = Product.objects.all()
        serializer = self.serializer_classes(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # def perform_create(self,serializer):

    #     return serializer.save(user= self.request.user,)

    # def get_queryset(self):
    #     products = Product.objects.all()
    #     serializer = self.serializer_class(products,many=True)
    #     return Response(serializer.data,status=status.HTTP_200_OK)
    
    
class UserProductListView(views.APIView):
    serializer_classes = ProductSerializer
    permission_classes = (permissions.AllowAny,)
    
    def post(self,request):
        username = request.data.get("id")
        products = Product.objects.filter(user__username=username)
        serializer = self.serializer_classes(products,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
        


class ProductAPIDetailView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get(self, request):
        id = request.data.get("id")
        product = get_object_or_404(self.queryset, id=id)
        product.views  += 1
        product.save()
        serializer = self.serializer_class(product, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductAPIPostView(views.APIView):
    serializer_class = AddProductSerializers
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        product = request.data
        serializer = self.serializer_class(data=product)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        product_data = serializer.data
        return Response(product_data, status=status.HTTP_201_CREATED)


class CategoryListView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Category.objects.filter(level=0)
    serializer_class = CategorySerializer


class CategoryProductsView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, general, subcategory=None):
        category = Category.objects.get(slug=general)
        if category.parent is not None:
            subcategory = category.slug
            general = category.parent.slug
        if subcategory:
            subcat = Category.objects.get(slug=subcategory)
            print(subcat.parent.id)
            products = Product.objects.filter(category__slug=subcategory)
            print(products)
        else:
            products = Product.objects.filter(category__parent__slug =general)
            

        serializer = self.serializer_class(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ImageBackgroundRemover(views.APIView):

    def post(self,request):
        pass
