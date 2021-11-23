from django.contrib import admin
from django.contrib.admin import site
from django.contrib import admin
from .models import Auction,AuctionBid,AuctionPlegde
# from apps.confi

class PrepAdmin(object):
   prepopulated_fields = {"slug": ("name",)}

class AuctionItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'amount', 'shipping_fee','category')
    list_filter = ('created', 'category', )
    date_hierarchy = 'created'
    search_fields = ('name',)
    raw_id_fields = ('image', )
    prepopulated_fields = {"slug_name": ("name",)}
    # inlines = [AuctionItemImagesInline, ]


class AutciotnBidAdmin(admin.ModelAdmin):
    list_display = ('auction', 'bidder', 'price')
    list_filter = ('created', )
    date_hierarchy = 'created'
    raw_id_fields = ('auction', 'bidder')


class AuctionPlegdeAdmin(admin.ModelAdmin):
    list_display = ('auction', 'profile', 'amount', 'created')
    list_filter = ('created', )
    raw_id_fields = ('auction', 'profile')
    date_hierarchy = 'created'


class AuctionAdmin(admin.ModelAdmin):
    list_display = ('product', 'status', 'backers', 'current_offer', )
    list_filter = ('status', 'created', )
    date_hierarchy = 'created'
    raw_id_fields = ('product', 'last_bidder_member', )


# class CategoryAdmin(PrepAdmin, admin.ModelAdmin):
#     prepopulated_fields = {"slug": ("name",)}
# class BrandADmin(PrepAdmin, admin.ModelAdmin):pass


site.register(Auction, AuctionAdmin)
# site.register(AuctionItem, AuctionItemAdmin)
site.register(AuctionBid, AutciotnBidAdmin)
site.register(AuctionPlegde, AuctionPlegdeAdmin)
# site.register(Brand)
# site.register(Category)


