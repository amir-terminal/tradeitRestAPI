AUCTION_WAITING = 'w'
AUCTION_PROCESSING = 'p'
AUCTION_PAUSE = 's'
AUCTION_JUST_ENDED = 'e'
AUCTION_FINISHED = 'f'
AUCTION_WAITING_PAYMENT = 'm'
AUCTION_PAID = 'd'
AUCTION_COMPLETED = 'c'

AUCTION_WAITING_PLEDGE = 'w'
AUCTION_FINISHED_NO_PLEDGED = 'x'
AUCTION_SHOWCASE = 'p'

BID_NORMAL = 'n'
BID_MATIC = 'm'


ORDER_WAITING_PAYMENT = 'wp'
ORDER_SHIPPING_FEE_REQUESTED = 'rf'
ORDER_PROCESSING_ORDER = 'rf'
ORDER_PAID = 'pd' # Processing Order
ORDER_DELIVERED = 'dl'
ORDER_WAITING_TESTIMONIAL = 'wt'



AUCTION_STATUS = (
    (AUCTION_WAITING_PLEDGE, "Waiting pledge"),
    (AUCTION_SHOWCASE, "Showcase"),
    (AUCTION_PAUSE, "Pause"),
    (AUCTION_JUST_ENDED, "Just Ended"),
    (AUCTION_FINISHED, "Finished"),
    (AUCTION_FINISHED_NO_PLEDGED, "Finished without pledged the price"),
    (AUCTION_WAITING_PAYMENT, "Waiting Payment"), #NEW
    (AUCTION_PAID, "Paid"),
    (AUCTION_COMPLETED, "Completed"),
)


BID_TYPE_CHOICES = (
    ("n", "Normal"),
    ("m", "bid-o-matic"),
)



# ORDER_WAITING_PAYMENT = 'wp'
# ORDER_SHIPPING_FEE_REQUESTED = 'rf'
# ORDER_PROCESSING_ORDER = 'rf'
# ORDER_DELIVERED = 'dl'
# ORDER_WAITING_TESTIMONIAL = 'wt'

# ORDER_STATUS = (
#     (ORDER_WAITING_PAYMENT, "Waiting Payment"),
#     (ORDER_SHIPPING_FEE_REQUESTED, "Shipping fee Requested"),
#     (ORDER_PROCESSING_ORDER, "Processing order"), #PAID
#     (ORDER_DELIVERED, "Delivered"),
#     (ORDER_WAITING_TESTIMONIAL, "Waiting Testimonial"),
# )
