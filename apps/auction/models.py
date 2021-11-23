from django.db import models

# Create your models here.
# -*- coding: utf-8 -*-



from time import time
from random import randint
from datetime import datetime

from django.db import models
from django.db.models import F
from django.db.models import Avg, Max, Min, Count
from django.core.validators import RegexValidator
from apps.product.models import Product
from .exceptions import *

# from utils import full_url
from .constants import *
from apps.account.models import Profile, User

class AuctionManager(models.Manager):
    def waiting_pledge(self):
        return self.get_query_set().filter(status=AUCTION_WAITING_PLEDGE)

    def time_over(self):
        return self.waiting_pledge().filter(deadline_time__lte=time())

    def showcase(self):
        return self.get_query_set().filter(status=AUCTION_SHOWCASE)

    def about_to_start(self):
        pass

    def public(self):
        return self.get_query_set().filter(status__in=[AUCTION_SHOWCASE, AUCTION_PAUSE, AUCTION_JUST_ENDED, AUCTION_WAITING_PLEDGE])

    def live(self):
        return self.get_query_set().filter(status__in=[AUCTION_SHOWCASE, AUCTION_PAUSE, AUCTION_JUST_ENDED])
        #return self.get_query_set().filter(status__in=['w', 'p', 's', 'e'])
    #def live(self):
    #    return self.get_query_set().filter(status__in=['w', 'p', 's', 'e'])

    #def running(self):
    #    return self.filter(status='p')

    def paused(self):
        return self.get_query_set().filter(status='p')

    #def waiting(self):
    #    return self.get_query_set().filter(status='w')

    def finished(self):
        return self.get_query_set().filter(status=AUCTION_FINISHED)


    def just_ended(self):
        return self.get_query_set().filter(status=AUCTION_JUST_ENDED)

    # def expired(self):
    #     return self.just_ended().filter(ended_unixtime__lte=time()-settings.MAX_TIME_HOMEPAGE)

    def about_end(self):
        return self.running().filter(last_unixtime__lte=time()-F('bidding_time'))

    def finish_expired(self):
        self.expired().update(status='f')

    def create_from_item(self, item):
        auction = Auction.objects.create(item=item, bidding_time=item.bidding_time, deadline_time=time()+item.pledge_time)
        item.amount -= 1
        item.save()
        return auction

class AuctionItemManager(models.Manager):
    def kick_off(self):
        items = self.get_query_set().exclude(code__in=Auction.objects.waiting_pledge().values_list('item', flat=True), amount__gt=0)
        i = randint(0, items.count()-1) #TODO check this
        item = items[i]
        return item
        #return Auction.objects.create_from_item(item)



class Auction(models.Model):
    product = models.ForeignKey(Product, related_name='auctions', db_index=True,on_delete=models.CASCADE)
    #status = models.CharField(max_length=1, default=AUCTION_WAITING_PLEDGE, choices=AUCTION_STATUS, db_index=True)
    status = models.CharField(max_length=2, default=AUCTION_WAITING_PLEDGE, choices=AUCTION_STATUS, db_index=True)

    #order_status = models.CharField(max_length=2, blank=True, null=True, choices=ORDER_STATUS, db_index=True)
    #waiting payment, processign order, upload testimonial

    amount_pleged = models.PositiveIntegerField(default=0)
    backers = models.PositiveIntegerField(default=0)
    current_offer = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    pledge_time =  models.PositiveIntegerField(default=43200)

    deadline_time = models.FloatField(db_index=True)
    bidding_time = models.PositiveSmallIntegerField()
    last_bidder = models.CharField(max_length=30, default='', db_index=True)
    last_bidder_member = models.ForeignKey(User, blank=True, null=True, related_name='items_won',on_delete=models.CASCADE)  #winner

    last_bid_type = models.CharField(max_length=1, default='n', choices=BID_TYPE_CHOICES, blank=True, null=True) #Todo remove this field
    last_unixtime = models.FloatField(null=True, blank=True, db_index=True)
    ended_unixtime = models.FloatField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    objects = AuctionManager()

    def __unicode__(self):
        return self.item.name

    # @models.permalink
    # def get_absolute_url(self):
    #     return 'auction_item', (), {'slug':self.item.slug_name}

    @property
    def time_to_go(self):
        if self.status != AUCTION_WAITING_PLEDGE:
            return -1
        return self.deadline_time - time()

    def pledge(self, member, amount):
        self.amount_pleged += amount
        if not AuctionPlegde.objects.filter(auction=self, member=member).exists():
            self.backers += 1
        AuctionPlegde.objects.create(auction=self, member=member, amount=amount)
        self.save()

    @property
    def is_processing(self):
        return self.status == AUCTION_SHOWCASE

    @property
    def is_waiting_pledge(self):
        return self.status == AUCTION_WAITING_PLEDGE

    @property
    def is_paused(self):
        return self.status == AUCTION_PAUSE

    @property
    def is_running(self):
        return self.is_processing or self.is_paused

    @property
    def funded(self):
        """returns the percent funded"""
        return self.amount_pleged * 100 / self.item.price

    @property
    def time_left(self):
        if not self.last_unixtime:
            return self.bidding_time
        return int(self.last_unixtime + self.bidding_time - time())
        #t = self.last_unixtime + self.bidding_time - time()
        return int(round(t+0.49))

    def end_dt(self):
        return datetime.fromtimestamp(int(self.last_unixtime))

    @property
    def is_ended(self):
        return self.ended_unixtime != None

    def end(self):
        self.status = AUCTION_JUST_ENDED
        self.ended_unixtime = time()
        if self.last_bidder_member:
            self.order_status = ORDER_WAITING_PAYMENT
        self.save()

    def pause(self):
        self.status = AUCTION_PAUSE
        self.save()

    def resume(self):
        if self.current_offer == 0.0:
            self.status = AUCTION_WAITING_PLEDGE
        else:
            self.status = AUCTION_SHOWCASE
        self.save()

    def bid_by(self, bidder):
        if self.status in ['f','m','d','c','e']:
            raise AuctionExpired

        username = bidder.user.username
        if bidder.credits <= 0:
            raise NotEnoughCredits

        if self.last_bidder == username:
            #TODO check this only raise without conditions, no win require, no conditions
            raise AlreadyHighestBid

        #if self.status == "w":
        #    raise AuctionIsNotReadyYet

        # Paused Auction Will still accept bid
        #elif self.status == "s":
        #    raise AuctionPaused

        bid_type = 'n'
        # price = self.current_offer + settings.PRICE_INTERVAL
        unixtime = time()
        if self.status == 'w':
            self.status = 'p'
        AuctionBid.objects.create(auction=self, bidder=bidder, unixtime=unixtime, price=price)
        self.last_bidder = username
        self.last_bidder_member = bidder.user
        self.last_bid_type = bid_type
        self.last_unixtime = time()
        self.current_offer = price
        self.save()

    @property
    def backers_history(self):
        from apps.account.models import User
        return User.objects.filter(auctionplegde__auction=self).distinct().annotate(pledge_date=Max('auctionplegde__created'))

    @property
    def bidding_history(self):
        return AuctionBid.objects.filter(auction=self).order_by('-created')

    def total_price(self):
        return self.current_offer + self.item.shipping_fee

class AuctionBid(models.Model):
    auction = models.ForeignKey(Auction,on_delete=models.CASCADE)
    bidder = models.ForeignKey(Profile,on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    unixtime = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s : %s ' %(self.auction, self.bidder)



class AuctionPlegde(models.Model):
    auction = models.ForeignKey(Auction,on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s %s' % (self.auction, self.profile)

