
# ------------------------------------------------------------ old models keept safe ------------------------------------

# """
# Category model
 
# """


# class Category(models.Model):
#     name = models.CharField(max_length=150, db_index=True)
#     slug = models.SlugField(max_length=150, unique=True, db_index=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ('-created_at',)
#         verbose_name = 'category'
#         verbose_name_plural = 'categories'

#     def __str__(self):
#         return self.name


# """
# Sub category model

# """


# class SubCategory(models.Model):
#     category = models.ForeignKey(
#         Category, on_delete=models.CASCADE, related_name='subcategories')
#     name = models.CharField(max_length=150, unique=True, db_index=True)
#     slug = models.SlugField(max_length=150, db_index=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ('-created_at',)
#         verbose_name = 'sub-category'

#     def __str__(self):
#         return self.name


# """ 
# Detail model

# """


# class Details(models.Model):
#     brand = models.CharField(max_length=100, blank=True)
#     model = models.CharField(max_length=100, blank=True)
#     size = models.IntegerField(blank=True)
#     year = models.DateField()


# """ 
# Products images Upload Function
# """


# def uploadmodel_file_upload_to(instance, filename):
#     return f'uploads/{instance.product.user.username}/products/{instance.product.title}_{instance.product.id}/{filename}'


# """ 
# Products model
# """


# class Product(models.Model):
#     condition_choises = [('new', 'never used'), ('good', 'used but functional'),
#                          ('refabrished', 'broken and fixed '), ('broken', 'does not work')]
#     photos = models.ImageField(upload_to=uploadmodel_file_upload_to)
#     user = models.OneToOneField(
#         User, related_name='products', on_delete=models.CASCADE)
#     title = models.CharField(max_length=150, db_index=True)
#     price = models.FloatField(blank=True, default=0.0)
#     slug = models.SlugField(max_length=150, db_index=True)
#     currancy = models.CharField(max_length=5, default='DZ')
#     tradable = models.BooleanField(default=False)
#     negotiable = models.BooleanField(default=False)
#     sold = models.BooleanField(default=False)
#     traded = models.BooleanField(default=False)
#     delivery = models.BooleanField(default=False)
#     description = models.TextField(blank=False)
#     views = models.IntegerField(default=0)

#     detail = models.ForeignKey(
#         Details, on_delete=models.SET_NULL, blank=True, null=True)
#     category = models.ForeignKey(
#         Category, related_name='products', on_delete=models.CASCADE)
#     subcategory = models.ForeignKey(
#         SubCategory, related_name='products', on_delete=models.CASCADE)
#     condition = models.CharField(
#         max_length=150, choices=condition_choises, db_index=True, default='new')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def views_auto_increaser(self):
#         self.views += 1
#         return self.views

#     class Meta:
#         ordering = ['-created_at',
#                     '-updated_at']

#     def __str__(self):
#         return self.title


# """ 
# Products images Upload Function
# """


# class Images(models.Model):
#     product = models.ForeignKey(
#         Product, on_delete=models.CASCADE, related_name='images')
#     image = models.ImageField(
#         upload_to=uploadmodel_file_upload_to, storage=OverwriteStorage())
#     default = models.BooleanField(default=False)
#     width = models.FloatField(default=100)
#     length = models.FloatField(default=100)

#     def default(self):
#         return self.images.filter(default=True).first()

#     def thumbnails(self):
#         return self.images.filter(width__lt=100, length_lt=100)

#     def __str__(self):
#         return self.product.title


# """
# Product Saving
# """


# class ProductSave(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)

#     class Meta:
#         unique_together = ("product", "user")

#     def __str__(self):
#         return 'Like: ' + self.user.username + ' ' + self.product.title







#___________________________________________________ Reusbale Code _______________________________________________________________


# class CategoryTreeSerializer(serializers.ModelSerializer):
#     children = serializers.SerializerMethodField(source='get_children')
#     class Meta:
#         fields = ('children',)  # add here rest of the fields from model 

#     def get_children(self, obj):
#         children = self.context['children'].get(obj.id, [])
#         serializer = CategoryTreeSerializer(children, many=True, context=self.context)
#         return serializer.data

 
# # views.py
# class CategoryViewSets(viewsets.ModelViewSet):
 
#     queryset = Category.objects.all()
#     serializer_class = CategoryTreeSerializer
 
#     @action(detail=True)
#     def tree(self, request, pk=None):
#         """
#         Detail route of an category that returns it's descendants in a tree structure.
#         """
#         category = self.get_object()
#         descendants = category.get_descendants() # add here any select_related/prefetch_related fields to improve api performance
 
#         children_dict = defaultdict(list)
#         for descendant in descendants:
#             children_dict[descendant.get_parent().pk].append(descendant)
 
#         context = self.get_serializer_context()
#         context['children'] = children_dict
#         serializer = CategoryTreeSerializer(category, context=context)
 
#         return Response(serializer.data)


""" 
Reusable code
commented. 
"""

# @receiver(models.signals.pre_save, sender=User)
# def auto_delete_file_on_change(sender, instance, **kwargs):
#     """
#     Deletes old file from filesystem
#    with new file.
#     """
#     print('posted image')
#      when corresponding `MediaFile` object is updated
#     if not instance.pk:
#         return False

#     try:
#         old_file = sender.objects.get(pk=instance.pk).avatar
#     except sender.DoesNotExist:
#         return False
#     if not instance.avatar.name == 'none.jpg':
#         new_file = instance.avatar
#         if not old_file == new_file:
#             if os.path.exists(old_file.path):
#                 print(f'image {old_file.path} has been removed')
#                 os.remove(old_file.path)





# class AuctionItemImages(models.Model):
#     item = models.ForeignKey(AuctionItem, related_name="images")
#     img = models.ImageField(help_text="default image 120px height 200px width recommended", upload_to="items")
#     is_default = models.BooleanField(default=False)

#     def __unicode__(self):
#         return unicode(self.img)

#     def get_full_url(self):
#         return full_url(self.img.url)

#     def save(self, *args, **kwargs):
#         super(AuctionItemImages, self).save(*args, **kwargs)
#         if self.is_default:
#             self.item.image = self
#             self.item.save()

#     class Meta:
#         verbose_name = u'auction item image'
#         verbose_name_plural = u'auction item images'
