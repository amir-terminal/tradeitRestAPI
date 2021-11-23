from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import (
    Category,
    Product,
    ProductImage,
    ProductSpecification,
    ProductSpecificationValue,
    ProductType,
)


admin.site.register(Category,MPTTModelAdmin)



class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [
        ProductSpecificationInline,
    ]
    # prepopulated_fields = {'slug':('name',)}



class ProductImageInline(admin.TabularInline):
    model = ProductImage


class ProductSpecificationValueInline(admin.TabularInline):
    model = ProductSpecificationValue


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ['views']
    inlines = [
        ProductSpecificationValueInline,
        ProductImageInline,
    ]
    list_display = ['title','category','user','price','created_at','updated_at','discount']
    list_editable = ['discount','price']






