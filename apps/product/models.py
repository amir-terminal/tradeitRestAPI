#___________________________________________________________________ Imports ____________________________________________________________________________________________

from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import AutoSlugField
from django.urls import reverse
from django.db import models
from apps.account.models import User, OverwriteStorage,Profile
import uuid
# import blurhash




# __________________________________________________________________________Category model _______________________________________________________________________________

# Catgories made with mptt because we need to have subcategories which i give them the related_name of subcategories


class Category(MPTTModel):
    """
    Category Table implimented with MPTT.
    """

    name = models.CharField(
        verbose_name=_("Category Name"),
        help_text=_("Required and unique"),
        max_length=255,
        unique=True,
    )
    slug = AutoSlugField(populate_from=['name', ], verbose_name=_(
        "Category safe URL"), max_length=255, unique=True,db_index=True)
    parent = TreeForeignKey("self", on_delete=models.CASCADE,
                            null=True, blank=True, related_name="subcategories")
    is_active = models.BooleanField(default=True)
    
    objects = models.Manager()
    tree = TreeManager()

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ("id",)

    def get_absolute_url(self):
        return reverse("product:category_list", args=[self.slug])

    def __str__(self):
        return self.name


# _____________________________________________________________________________ Products Type and his detail _____________________________________________________________


class ProductType(models.Model):
    """
    ProductType Table will provide a list of the different types
    of products that are for sale.
    """
    category = models.ForeignKey(Category,related_name='product_type_category',on_delete=models.CASCADE,blank=True)
    name = models.CharField(verbose_name=_("Product Name"), help_text=_(
        "Required"), max_length=255, unique=True)
    slug = AutoSlugField(populate_from=['name', ], max_length=150,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Product Type")
        verbose_name_plural = _("Product Types")

    def __str__(self):
        return self.name


class ProductSpecification(models.Model):
    """
    The Product Specification Table contains product
    specifiction or features for the product types.
    """

    product_type = models.ForeignKey(
        ProductType, on_delete=models.RESTRICT, related_name="product_type")
    name = models.CharField(verbose_name=_(
        "Name"), help_text=_("Required"), max_length=255,)

    class Meta:
        verbose_name = _("Product Specification")
        verbose_name_plural = _("Product Specifications")

    def __str__(self):
        return self.name


# _____________________________________________Products model_____________________________________________________________________________________________________________


class Product(models.Model):
    """
    The Product table contining all product items.
    """
    
    condition_choises = [('new', 'New'), ('used', 'Used'),
                         ('refabrished', 'refabrished'), ('broken', 'Broken')]
    product_type = models.ForeignKey(
        ProductType, on_delete=models.RESTRICT, related_name='products')
    user = models.ForeignKey(
        User, related_name='products', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='products')
    title = models.CharField(
        verbose_name=_("title"),
        help_text=_("Required"),
        max_length=255,
    )
    description = models.TextField(verbose_name=_(
        "description"), help_text=_("Not Required"), blank=True)
    slug = AutoSlugField(
        populate_from=['id',], max_length=255, unique=True)
    currancy = models.CharField(max_length=5, default='DZ')
    tradable = models.BooleanField(default=False)
    negotiable = models.BooleanField(default=False)
    sold = models.BooleanField(default=False)
    traded = models.BooleanField(default=False)
    delivery = models.BooleanField(default=False)
    users_saved = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="user_saved", blank=True)
    tags = models.CharField(max_length=255,)
    price = models.DecimalField(
        verbose_name=_("Product price"),
        help_text=_("Maximum 99999999.99"),
        error_messages={
            "name": {
                "max_length": _("The price must be between 0 and 9999999999.99."),
            },
        },
        max_digits=12,
        decimal_places=2,
    )
    discount = models.DecimalField(
        verbose_name='discount persentage', max_digits=3, decimal_places=0, default=0)
    is_active = models.BooleanField(
        verbose_name=_("Product visibility"),
        help_text=_("Change product visibility"),
        default=True,
    )
    views = models.SmallIntegerField(default=0)

    condition = models.CharField(
        max_length=150, choices=condition_choises, db_index=True, default='new')
    created_at = models.DateTimeField(
        _("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        ordering = ("-created_at", '-updated_at')
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def views_auto_increaser(self):
        self.views += 1
        return self.views

    def get_absolute_url(self):
        return reverse("app:product_detail", args=[self.slug])

    def __str__(self):
        return self.title


# ___________________________________________________________________________________ Image Uploader Function and Model for the Product model ______________________________________________________________
""" 
Products images Upload Function
"""


def uploadmodel_file_upload_to(instance, filename):
    ext = filename.split('.')
    filename = str(uuid.uuid4())+'.jpg'
    return f'uploads/{instance.product.user.username}/products/{instance.product.title}_{instance.product.id}/{filename}'


class ProductImage(models.Model):
    """
    The Product Image table.
    """


    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(
        verbose_name=_("image"),
        help_text=_("Upload a product image"),
        upload_to=uploadmodel_file_upload_to, storage=OverwriteStorage(),
        default="images/default.png",
    )
    alt_text = models.CharField(
        verbose_name=_("Alturnative text"),
        help_text=_("Please add alturnative text"),
        max_length=255,
        null=True,
        blank=True,
        )
    is_feature = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    def thumbnails(self):
        return self.i.filter(width__lt=100, length_lt=100)

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")


# _____________________________________________________________________ Code Related to the producttype and specefication value______________________________________________________________________________


class ProductSpecificationValue(models.Model):
    """
    The Product Specification Value table holds each of the
    products individual specification or bespoke features.
    """

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='details')
    specification = models.ForeignKey(
        ProductSpecification, on_delete=models.RESTRICT, related_name='specification')
    value = models.CharField(
        verbose_name=_("value"),
        help_text=_("Product specification value (maximum of 255 words"),
        max_length=255,
    )
    class Meta:
        verbose_name = _("Product Specification Value")
        verbose_name_plural = _("Product Specification Values")
    def __str__(self):
        return self.value


