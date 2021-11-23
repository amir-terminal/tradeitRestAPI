"""************************************ Imports ***************************** """
from rest_framework.fields import ImageField, SerializerMethodField
from apps.account.models import Location, Profile, User
from rest_framework import serializers
from rest_framework.relations import ManyRelatedField
from rest_framework_recursive.fields import RecursiveField
from .models import Category, Product, ProductImage, ProductSpecificationValue, ProductType
from apps.account.serializers import ProfileSerializer, UserSerializer
# Product

# _______________________________________________Code_______________________________________________________________________





class CategorySerializer(serializers.ModelSerializer):
    subcategories = RecursiveField(many=True)
    class Meta:
        model = Category
        fields = ['name', 'slug', 'is_active', 'subcategories', ]


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ['name', ]


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','']

class ProductSpecificationValueSerializer(serializers.ModelSerializer):
    # product_type = serializers.CharField(source='producttype.name')
    specification = serializers.StringRelatedField(many=False)

    class Meta:
        model = ProductSpecificationValue
        fields = ('specification', 'value')


class ProductImagesSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_image_url')
    class Meta:
        model = ProductImage
        fields = ['image', 'is_feature']
        
    def image(self, obj):
        return obj.image.url
    
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['country','city','zipcode','address']


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.parent')
    sub_category = serializers.CharField(source='category.name')
    details = ProductSpecificationValueSerializer(many=True)
    images = ProductImagesSerializer(many=True)
    productType = serializers.StringRelatedField(source='product_type')
    timePosted = serializers.DateTimeField(source='created_at')
    user = UserSerializer()
    
    class Meta:
        model = Product
        fields = ['id', 'user', 'price', 'title', 'slug', 'timePosted', 'category', 'sub_category','views',
                  'condition', 'delivery', 'tradable','negotiable', 'description', 'currancy', 'productType', 'details', 'images']

    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        product.save()
        return product



class AddProductSerializers(serializers.ModelSerializer):
    details = ProductSpecificationValueSerializer(many=True)
    images = ProductImagesSerializer()
    productType = serializers.StringRelatedField(source='product_type')
    
    class Meta:
        model = Product
        fields = ['title','price','title','slug','category','productType','condition','negotiable','tradable','delivery','details','images']
    
class ProductListSerializer(serializers.ModelSerializer):
    details = ProductSpecificationValueSerializer(many=True)
    thumbnail = serializers.SerializerMethodField('get_tumbnail')
    productType = serializers.StringRelatedField(source='product_type')
    category = serializers.CharField(source='category.name')
    
    class Meta:
        model = Product
        fields = ['id','title','price','slug','views','category','productType','user','condition','negotiable','tradable','delivery','details','thumbnail']
        
    def get_tumbnail(self, obj):
        image = obj.images.get(is_feature = True).image.url
        return image